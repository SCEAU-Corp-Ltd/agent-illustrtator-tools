#!/usr/bin/env python3
"""Tiny local HTTP listener for MCP/MCPO callback experiments."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


REDACTED_HEADERS = {"authorization", "cookie", "x-api-key", "x-auth-token"}
DEFAULT_EVENTS_PATH = Path(".tmp/listener-events.jsonl")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact_headers(headers: Any) -> dict[str, str]:
    clean: dict[str, str] = {}
    for key, value in headers.items():
        clean[key] = "[redacted]" if key.lower() in REDACTED_HEADERS else value
    return clean


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"raw": line})
    return events


def build_event(handler: BaseHTTPRequestHandler, body: bytes) -> dict[str, Any]:
    parsed_url = urlparse(handler.path)
    text_body = body.decode("utf-8", errors="replace")
    parsed_body: Any = None

    content_type = handler.headers.get("content-type", "")
    if text_body and "application/json" in content_type.lower():
        try:
            parsed_body = json.loads(text_body)
        except json.JSONDecodeError:
            parsed_body = None

    return {
        "receivedAt": utc_now(),
        "method": handler.command,
        "path": parsed_url.path,
        "query": parse_qs(parsed_url.query),
        "headers": redact_headers(handler.headers),
        "bodyText": text_body,
        "bodyJson": parsed_body,
        "client": handler.client_address[0],
    }


class ListenerHandler(BaseHTTPRequestHandler):
    events_path: Path = DEFAULT_EVENTS_PATH

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{utc_now()} {self.client_address[0]} {format % args}")

    def send_json(self, status: int, payload: dict[str, Any] | list[Any]) -> None:
        data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def append_event(self, event: dict[str, Any]) -> None:
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, sort_keys=True))
            stream.write("\n")

    def read_body(self) -> bytes:
        length = int(self.headers.get("content-length", "0") or "0")
        return self.rfile.read(length) if length else b""

    def capture(self) -> None:
        event = build_event(self, self.read_body())
        self.append_event(event)
        self.send_json(200, {"ok": True, "event": event})

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/health":
            self.send_json(200, {"ok": True, "time": utc_now()})
            return
        if parsed_url.path == "/events":
            self.send_json(200, {"events": read_events(self.events_path)})
            return
        if parsed_url.path == "/events/latest":
            events = read_events(self.events_path)
            self.send_json(200, {"event": events[-1] if events else None})
            return
        self.capture()

    def do_POST(self) -> None:
        self.capture()

    def do_PUT(self) -> None:
        self.capture()

    def do_PATCH(self) -> None:
        self.capture()

    def do_DELETE(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/events":
            if self.events_path.exists():
                self.events_path.unlink()
            self.send_json(200, {"ok": True, "eventsCleared": True})
            return
        self.capture()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a local HTTP listener for MCP/MCPO experiments."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--events", default=str(DEFAULT_EVENTS_PATH))
    args = parser.parse_args()

    ListenerHandler.events_path = Path(args.events)
    server = ThreadingHTTPServer((args.host, args.port), ListenerHandler)
    print(f"Listening on http://{args.host}:{args.port}")
    print(f"Writing events to {ListenerHandler.events_path}")
    server.serve_forever()


if __name__ == "__main__":
    main()

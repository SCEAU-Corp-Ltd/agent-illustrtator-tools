#!/usr/bin/env python3
"""Local vision LLM calls via Ollama /api/chat (stdlib only).

Env (optional):
  OLLAMA_BASE_URL - default http://127.0.0.1:11434
  OLLAMA_HOST - used if OLLAMA_BASE_URL unset
  OLLAMA_MODEL - default model tag, default llava

Pull a vision tag first, e.g. `ollama pull llava`, `ollama pull qwen2.5vl:7b`,
or `ollama pull gemma3:4b`; see `ollama list` for exact names and
`workflows/ollama-qwen-gemma-vision.md` for Qwen/Gemma presets.

CLI:
  python3 tools/ollama-vision/ollama_vision.py -p "..." -i ./x.png

Library:
  from ollama_vision import vision_chat, describe_image
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llava"
DEFAULT_DESCRIBE_PROMPT = (
    "Describe this image clearly and concisely for someone automating "
    "graphic design: main subjects, colors, layout, and any visible text."
)


def default_base_url() -> str:
    return (
        os.environ.get("OLLAMA_BASE_URL") or os.environ.get("OLLAMA_HOST") or DEFAULT_BASE_URL
    ).rstrip("/")


def default_model() -> str:
    return os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL


def image_to_base64(data: bytes) -> str:
    return base64.standard_b64encode(data).decode("ascii")


def normalize_image_to_base64(image: str | Path | bytes) -> str:
    """Return raw standard base64 (no data: prefix) for the Ollama REST API."""
    if isinstance(image, bytes):
        return image_to_base64(image)

    s = str(image).strip()
    path = Path(os.path.expanduser(s))

    if path.is_file():
        return image_to_base64(path.read_bytes())

    image_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif"}
    if path.suffix.lower() in image_suffixes and len(s) < 2048 and not path.is_file():
        raise FileNotFoundError(f"Image path not found: {path}")

    data_url = re.match(
        r"^data:(?P<mime>[\w/+.-]+);base64,(?P<b64>[A-Za-z0-9+/=\s]+)$",
        s,
        re.IGNORECASE,
    )
    if data_url:
        raw = re.sub(r"\s+", "", data_url.group("b64"))
        base64.standard_b64decode(raw)
        return raw

    raw = re.sub(r"\s+", "", s)
    base64.standard_b64decode(raw)
    return raw


def vision_chat(
    prompt: str,
    *,
    images: list[str | Path | bytes] | None = None,
    model: str | None = None,
    base_url: str | None = None,
    system: str | None = None,
    stream: bool = False,
    timeout: float = 300.0,
) -> str:
    """Send multimodal chat to Ollama; return assistant message text."""
    url = f"{(base_url or default_base_url()).rstrip('/')}/api/chat"
    m = model or default_model()
    b64_images = [normalize_image_to_base64(img) for img in (images or [])]

    messages: list[dict[str, Any]] = []
    if system:
        messages.append({"role": "system", "content": system})
    user_msg: dict[str, Any] = {"role": "user", "content": prompt}
    if b64_images:
        user_msg["images"] = b64_images
    messages.append(user_msg)

    payload = {"model": m, "messages": messages, "stream": stream}

    body = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {detail or exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"Ollama connection failed: {exc.reason}") from exc

    msg = data.get("message") or {}
    content = msg.get("content")
    if not content:
        raise RuntimeError(f"Unexpected Ollama response: {json.dumps(data)[:800]}")
    return str(content).strip()


def describe_image(
    image: str | Path | bytes,
    *,
    prompt: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    system: str | None = None,
    timeout: float = 300.0,
) -> str:
    """One image with default description-oriented prompt."""
    return vision_chat(
        prompt or DEFAULT_DESCRIBE_PROMPT,
        images=[image],
        model=model,
        base_url=base_url,
        system=system,
        timeout=timeout,
    )


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Call Ollama /api/chat with optional vision images (base64 in JSON).",
    )
    parser.add_argument(
        "--prompt",
        "-p",
        default=DEFAULT_DESCRIBE_PROMPT,
        help="User message (default: design-oriented describe prompt).",
    )
    parser.add_argument(
        "--image",
        "-i",
        action="append",
        dest="images",
        metavar="PATH",
        help="Image path (repeat for multiple).",
    )
    parser.add_argument(
        "--image-base64",
        action="append",
        dest="b64_images",
        metavar="B64",
        help="Raw base64 (repeat for multiple).",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=None,
        help=f"Model tag (default: env OLLAMA_MODEL or {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--base-url",
        "-u",
        default=None,
        help=f"Ollama base URL (default: env or {DEFAULT_BASE_URL}).",
    )
    parser.add_argument("--system", "-s", default=None, help="Optional system message.")
    parser.add_argument("--json", action="store_true", help='Print JSON {"response": ...}.')
    args = parser.parse_args(argv)

    imgs: list[str | Path | bytes] = []
    if args.images:
        imgs.extend(args.images)
    if args.b64_images:
        imgs.extend(args.b64_images)

    if not imgs:
        parser.error("Provide at least one --image and/or --image-base64.")

    try:
        out = vision_chat(
            args.prompt,
            images=imgs,
            model=args.model,
            base_url=args.base_url,
            system=args.system,
        )
    except (RuntimeError, OSError, ValueError, binascii.Error) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"response": out}, ensure_ascii=False))
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())


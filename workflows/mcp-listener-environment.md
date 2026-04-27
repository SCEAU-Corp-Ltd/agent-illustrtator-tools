# MCP Listener Environment

Use this workflow to understand local listener behavior before wiring anything
to Illustrator, MCP, MCPO, or another live tool.

## What This Is

`tools/listener-playground/listener.py` is a small local HTTP listener. It
accepts any `GET`, `POST`, `PUT`, `PATCH`, or `DELETE` request, records the
method/path/headers/body, and returns JSON. It is meant for inspection and
 debugging, not a live service.

Runtime events are written to `.tmp/listener-events.jsonl`, which is ignored by
Git.

## Mental Model

- MCP over stdio does not expose an HTTP listener by itself.
- MCPO or another bridge can expose MCP tools through HTTP.
- A listener is useful when you need to inspect callbacks, webhook-shaped
  payloads, local bridge requests, or tool events.
- Keep the listener on `127.0.0.1` while testing so it is not exposed to the
  network.

## Run

From the repository root:

```powershell
python tools\listener-playground\listener.py --host 127.0.0.1 --port 8765
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/health
```

Send a test event:

```powershell
powershell -ExecutionPolicy Bypass -File tools\listener-playground\send-test-event.ps1
```

See the latest captured event:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/events/latest
```

Clear captured events:

```powershell
Invoke-RestMethod -Method Delete http://127.0.0.1:8765/events
```

## Useful Paths

| Endpoint | Purpose |
|---|---|
| `/health` | Confirms the listener is running. |
| `/events` | Returns captured events. |
| `/events/latest` | Returns the latest captured event. |
| Any other path | Captures the incoming request and returns it as JSON. |

## MCPO Debug Loop

1. Start this listener.
2. Start the MCP or MCPO process in a separate terminal.
3. Point any webhook, callback, or test HTTP target at
   `http://127.0.0.1:8765/<name-you-want>`.
4. Trigger one action.
5. Inspect `/events/latest`.
6. Only after the payload is understood, connect it to the real target.

## Safety

- Do not bind to `0.0.0.0` unless you intentionally want LAN exposure.
- Do not paste real tokens into test payloads.
- Do not commit `.tmp/` output.
- Redact private paths and headers before copying listener output into docs.

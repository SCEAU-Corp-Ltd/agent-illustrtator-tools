# Listener Playground

Small local HTTP listener for MCP/MCPO experiments.

Run from the repository root:

```powershell
python tools\listener-playground\listener.py --host 127.0.0.1 --port 8765
```

Send a sample event:

```powershell
powershell -ExecutionPolicy Bypass -File tools\listener-playground\send-test-event.ps1
```

Inspect the latest event:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/events/latest
```

The full workflow is documented in
`workflows/mcp-listener-environment.md`.

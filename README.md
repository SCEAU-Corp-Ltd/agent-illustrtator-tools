# Agent-Illustrtator-Tools

Public notes and examples for using Adobe Illustrator MCP server tools.

## Contents

| Path | Purpose |
|---|---|
| `docs/adobe-illustrator-mcp-tools.md` | Current Illustrator MCP function snapshot. |
| `tools/listener-playground/` | Local HTTP listener for MCP/MCPO event experiments. |
| `workflows/illustrator-recolor.md` | Practical recolor workflow using appearance and QA tools. |
| `workflows/mcp-listener-environment.md` | How to run and reason about the listener playground. |

## Use

Use the docs as generic operating references for MCP server tools.

## Illustrator MCP Snapshot

The current documented Adobe Illustrator MCP surface has 43 exposed callable
functions. See `docs/adobe-illustrator-mcp-tools.md` for the full table,
attributes, and safety notes.

For recoloring work, use `workflows/illustrator-recolor.md`. It turns
`SetAppearance`, `GetVisualAppearance`, preview, preflight, and export tools
into a repeatable sequence.

For MCP/MCPO listener experiments, use `workflows/mcp-listener-environment.md`.

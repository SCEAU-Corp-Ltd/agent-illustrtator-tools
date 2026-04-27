# Agent-Illustrtator-Tools

Public notes and examples for using Adobe Illustrator MCP server tools with
Codex.

This workflow has been used for AI-run automated coloring: Illustrator tools
come from the Adobe MCP server, and automation is handled through Codex.

This depends on Adobe Illustrator (Beta). Adobe documents the MCP server as a
Beta feature for connecting desktop AI tools, including Codex, to Illustrator
(Beta).

## Contents

| Path | Purpose |
|---|---|
| `CONTRIBUTING.md` | Public contribution rules. |
| `SECURITY.md` | How to report safety or disclosure issues. |
| `docs/ai-tool-connections.md` | Notes for Codex, Claude Code, Cursor, and other AI tools. |
| `docs/adobe-illustrator-mcp-tools.md` | Current Illustrator MCP function snapshot. |
| `docs/public-boundary.md` | What belongs here and what stays private. |
| `tools/listener-playground/` | Local HTTP listener for MCP/MCPO event experiments. |
| `workflows/illustrator-recolor.md` | Practical recolor workflow using appearance and QA tools. |
| `workflows/mcp-listener-environment.md` | How to run and reason about the listener playground. |

## Use

Use the docs as generic operating references for MCP server tools.

For other AI tools, including Claude Code, Cursor, or another MCP-compatible
client, use the same Adobe MCP server concept and ask that AI tool to adapt the
workflow and connection steps to its own MCP configuration format.

## Scope

- AI-assisted Illustrator automation
- Adobe MCP server tools exposed by Illustrator (Beta)
- Codex-driven tool calls and workflow orchestration
- Automated coloring and recoloring examples

## Adobe MCP Docs

- [About using desktop AI tools with Adobe Illustrator (Beta)](https://helpx.adobe.com/au/illustrator/desktop/connect-with-other-apps-and-tools/about-using-ai-tools-with-illustrator.html)
- [Connect Adobe Illustrator (Beta) to AI tools](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/connect-illustrator-to-ai-tools.html)
- [Work with Adobe Illustrator (Beta) documents from AI tools](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/work-with-illustrator-documents-from-ai-tools.html)

## Public Boundary

This repo is for public implementation notes only. Project files, private
profiles, local MCP keys, private screenshots, and client-specific workflow
details should stay outside the repo. See `docs/public-boundary.md`.

## Illustrator MCP Snapshot

The current documented Adobe Illustrator MCP surface has 43 exposed callable
functions. See `docs/adobe-illustrator-mcp-tools.md` for the full table,
attributes, and safety notes.

For recoloring work, use `workflows/illustrator-recolor.md`. It turns
`SetAppearance`, `GetVisualAppearance`, preview, preflight, and export tools
into a repeatable sequence.

For MCP/MCPO listener experiments, use `workflows/mcp-listener-environment.md`.

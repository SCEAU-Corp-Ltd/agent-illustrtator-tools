# Agent Illustrator Tools

**Public repo:** [github.com/SCEAU-Corp-Ltd/agent-illustrator-tools](https://github.com/SCEAU-Corp-Ltd/agent-illustrator-tools) · open-source · safe to fork or clone.

This repository explains how to use AI assistants with **Adobe Illustrator (Beta)** using Adobe's MCP connection.

If you are **not a developer**, start here:

- `docs/non-developer-start-here.md` (plain-language guide)
- `workflows/illustrator-recolor.md` (step-by-step recolor workflow)

If you are setting up a specific AI tool, use:

- `docs/ai-tool-connections.md` (includes Adobe's newer "Adobe for creativity" connector path for Claude)

## What This Repo Is

- A documentation repo with workflows and safety guidance
- A reference for Illustrator MCP tooling and menu command values
- Example platform listing metadata files
- Optional local helper scripts for testing and visual QA

## What This Repo Is Not

- Not an Adobe product
- Not a plugin that you install inside Illustrator
- Not a place to store private keys, client files, or internal project details

## Prerequisites

| Requirement | Purpose |
| --- | --- |
| [Adobe Illustrator (Beta)](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/about-using-ai-tools-with-illustrator.html) with MCP enabled | Illustrator MCP tool calls |
| An MCP-capable assistant | Runs automation; see `docs/ai-tool-connections.md` |
| Git (optional) | Needed only if you want a local copy or want to contribute |

**Python 3.9+** is optional. Scripts under `tools/` use the Python standard library only—there is no `npm`/`pip` dependency install step for this repository.

Optional **local vision** (PNG review or design QA — stays on your machine):

- Install [Ollama](https://ollama.com), pull a vision tag (`ollama pull llava`, or **Qwen / Gemma**: [`workflows/ollama-qwen-gemma-vision.md`](workflows/ollama-qwen-gemma-vision.md)), then follow **`workflows/design-qa-with-ollama.md`** after each MCP export you care about.

## Quickstart

1. **Clone this repository**

   ```bash
   git clone https://github.com/SCEAU-Corp-Ltd/agent-illustrator-tools.git
   cd agent-illustrator-tools
   ```

2. **Connect Illustrator (Beta) to your assistant** using Adobe’s guides under [Adobe MCP Docs](#adobe-mcp-docs). Keep MCP URLs, bearer tokens, and API keys in your assistant settings or another private store—not in commits ([`docs/public-boundary.md`](docs/public-boundary.md)).

3. **Read docs for your path** — start with `docs/ai-tool-connections.md`. For Illustrator Claw, continue with `docs/illustrator-claw-public-setup.md` then `docs/illustrator-claw-automation-blueprints.md`.

4. **Run a concrete MCP workflow** — use **`workflows/illustrator-recolor.md`** for recolor steps. Where noted there, attach **`workflows/design-qa-with-ollama.md`** (and optionally **`workflows/ollama-qwen-gemma-vision.md`** for Qwen/Gemma-specific setup) so local vision QA is part of the same loop.

5. **Optional — MCP listener** (inspect HTTP-shaped callbacks before wiring MCP/MCPO bridges):

   ```bash
   python3 tools/listener-playground/listener.py --host 127.0.0.1 --port 8765
   curl -s http://127.0.0.1:8765/health
   ```

   More detail and PowerShell examples: `workflows/mcp-listener-environment.md`.

6. **Optional — Ollama vision on exported PNGs** (after step 4 when you have a preview file):

   ```bash
   ollama pull llava
   # Optional: copy .env.example and set OLLAMA_MODEL / OLLAMA_BASE_URL.

   python3 tools/ollama-vision/ollama_vision.py \
     --prompt "Summarize colors and layout; flag clipping, misalignment, or unreadable text." \
     --image ./preview.png
   ```

   Full loop (before/after, base64): **`workflows/design-qa-with-ollama.md`**.
   **Qwen2.5-VL or Gemma 3** tags and examples: **`workflows/ollama-qwen-gemma-vision.md`**.

## Paths by Audience

### Non-developers

- `docs/non-developer-start-here.md` - plain-language onboarding
- `workflows/illustrator-recolor.md` - practical recolor checklist
- `docs/public-boundary.md` - what must stay private

### AI-tool setup users

- `docs/ai-tool-connections.md`
- `docs/illustrator-claw-public-setup.md`
- `docs/illustrator-claw-automation-blueprints.md`

### Technical reference users

- `docs/adobe-illustrator-mcp-tools.md`
- `docs/illustrator-menu-command-links.md`
- `data/illustrator-menu-commands.csv`

## Platform Listings

| Platform | Listing file | Skill ref |
|---|---|---|
| ClawhHub | `clawhub.yaml` | `$illustrator-claw` |
| OpenClaw | `skills/illustrator-claw/agents/openclaw.yaml` | `$illustrator-claw` |
| Codex (OpenAI) | `skills/illustrator-claw/agents/openai.yaml` | `$illustrator-claw` |
| Claude Code | `skills/illustrator-claw/agents/claude.yaml` | `$illustrator-claw` |
| Adobe Exchange | `adobe-exchange.yaml` | — |

## Configuration

Browsing the docs requires no configuration.

For **secrets** (MCP tokens, cloud model keys, private hostnames), use your assistant’s configuration, Illustrator Claw private settings, or environment variables on your machine. Optional `OLLAMA_*` variables for the vision helper are listed in [`.env.example`](.env.example).

## Troubleshooting

- **MCP will not connect** — Confirm Illustrator (Beta) MCP is enabled and follow Adobe’s current “Connect Illustrator to AI tools” flow; verify tokens never land in Git.
- **Listener: address already in use** — Choose another `--port` (for example `8766`).
- **Ollama: connection refused** — Ensure the Ollama app or `ollama serve` is running and that `OLLAMA_BASE_URL` matches (default `http://127.0.0.1:11434`).

## Contents

| Path | Purpose |
|---|---|
| `CONTRIBUTING.md` | Public contribution rules. |
| `docs/non-developer-start-here.md` | Plain-language onboarding for non-developers. |
| `.env.example` | Commented optional `OLLAMA_*` defaults for `tools/ollama-vision/`. |
| `SECURITY.md` | How to report safety or disclosure issues. |
| `data/` | Public reference data used by the docs. |
| `docs/ai-tool-connections.md` | Notes for Codex, Claude Code, Cursor, and other AI tools. |
| `docs/adobe-illustrator-mcp-tools.md` | Current Illustrator MCP function snapshot. |
| `docs/illustrator-menu-command-links.md` | Searchable Illustrator menu command value index. |
| `docs/illustrator-claw-public-setup.md` | Generic Illustrator Claw setup guide for this repo. |
| `docs/illustrator-claw-automation-blueprints.md` | Public Illustrator Claw automation ideas and prompt starters. |
| `docs/public-boundary.md` | What belongs here and what stays private. |
| `skills/illustrator-claw/SKILL.md` | Codex skill for public-safe Illustrator Claw workflows. |
| `tools/listener-playground/` | Local HTTP listener for MCP/MCPO event experiments. |
| `tools/ollama-vision/` | Stdlib helper for local vision models via Ollama (`llava`, `qwen2.5vl`, `gemma3`, etc.). |
| `tools/build-menu-command-links.py` | Rebuilds the generated menu command index. |
| `workflows/illustrator-recolor.md` | Practical recolor workflow using appearance and QA tools. |
| `workflows/design-qa-with-ollama.md` | MCP export → local Ollama vision QA loop (optional). |
| `workflows/ollama-qwen-gemma-vision.md` | Qwen2.5-VL / Gemma 3 vision presets and commands (optional). |
| `workflows/mcp-listener-environment.md` | How to run and reason about the listener playground. |

## Use

Use this repo as a shared guide. Choose the path that matches your role:

- Non-technical user: read `docs/non-developer-start-here.md`
- Setup user: read `docs/ai-tool-connections.md`
- Advanced user: read `docs/adobe-illustrator-mcp-tools.md`

## Scope

- AI-assisted Illustrator automation
- Adobe MCP server tools exposed by Illustrator (Beta)
- Codex-driven tool calls and workflow orchestration
- Illustrator Claw-style public setup and automation patterns
- Illustrator menu command reference data
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
into a repeatable sequence. Add `workflows/design-qa-with-ollama.md` (and optionally
`workflows/ollama-qwen-gemma-vision.md` for **Qwen** or **Gemma** vision tags) when you
want **local** vision review of exported PNGs (Ollama).

For MCP/MCPO listener experiments, use `workflows/mcp-listener-environment.md`.

## Menu Command Reference

The repo includes a public Illustrator menu command reference copied from the
MIT-licensed AiCommandPalette data set:

- `data/illustrator-menu-commands.csv`
- `docs/illustrator-menu-command-links.md`

Use the command `value` fields only after checking document, selection, and
version requirements.

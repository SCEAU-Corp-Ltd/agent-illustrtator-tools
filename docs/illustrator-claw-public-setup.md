# Illustrator Claw Public Setup

Use this guide to connect your own Illustrator Claw agent runner to this public
Illustrator automation repository.

This file is intentionally generic. Do not copy private hostnames, account
names, bearer tokens, local absolute paths, client documents, screenshots, or
agent logs into this repo.

## What You Need

- A working Illustrator Claw install or hosted Illustrator Claw workspace.
- Access to an AI model provider configured in your own private Illustrator Claw
  settings.
- Git access to this repository.
- Adobe Illustrator (Beta) with its MCP server enabled for Illustrator-specific
  workflows.
- A private place for secrets, such as environment variables, your operating
  system keychain, or your Illustrator Claw secret store.

## Get The Repo

Clone the public repository and use it as the Illustrator Claw workspace:

```bash
git clone https://github.com/SCEAU-Corp-Ltd/agent-illustrator-tools.git
cd agent-illustrator-tools
```

The agent should read `README.md`, `docs/public-boundary.md`,
`docs/adobe-illustrator-mcp-tools.md`, and the workflow files before making
changes.

## Connect Illustrator Claw

1. Create or open an Illustrator Claw workspace that points at this checkout.
2. Give the agent read access to the repo.
3. Give write access only when you want the agent to edit docs, workflows, or
   tooling.
4. Add any MCP servers in your private Illustrator Claw settings, not in this repo.
5. Store API keys, bearer tokens, and local MCP connection strings in your
   private secret store.
6. Run a short verification task before asking for real work.

Private values to set locally:

| Value | Purpose | Commit it? |
|---|---|---|
| Workspace path | Tells Illustrator Claw where this repo is checked out. | No |
| Model provider key | Lets Illustrator Claw call your AI model provider. | No |
| Illustrator MCP URL | Lets Illustrator Claw reach your local Illustrator MCP server. | No |
| Illustrator MCP bearer token | Authenticates local MCP calls. | No |
| Export/output folder | Keeps generated files out of this public repo. | No |

Use your Illustrator Claw version's actual settings format. If you use a `.env` file,
keep it local and untracked.

Minimal verification prompt:

```text
Read README.md, docs/public-boundary.md, and docs/adobe-illustrator-mcp-tools.md.
Report which files explain the public safety boundary and which Illustrator MCP
tools are documented. Do not edit files.
```

## Connect Illustrator MCP

1. Open Adobe Illustrator (Beta).
2. Enable or start the Illustrator MCP server using Adobe's current
   instructions.
3. Copy the local MCP endpoint and bearer token into your private Illustrator Claw MCP
   configuration.
4. Restart or reload the Illustrator Claw agent runner if your setup requires it.
5. Ask Illustrator Claw to list available MCP tools.
6. Test on a blank or disposable Illustrator file first.

The first useful live check is:

```text
List open Illustrator documents. If a document is open, get the active artboard,
capture a preview, and run preflight checks. Do not modify artwork.
```

## Use Menu Commands

This repo includes public menu command reference data from AiCommandPalette:

- `data/illustrator-menu-commands.csv`
- `docs/illustrator-menu-command-links.md`

Use the `value` field when your automation surface supports Illustrator menu
command execution. Treat the command table as reference data, not a guarantee
that every command is available in every Illustrator version.

Rules for agents:

- Check `docRequired` before running a command that needs an open document.
- Check `selRequired` before running a command that needs selected artwork.
- Respect `minVersion` and `maxVersion`.
- Avoid rows marked `ignore` unless you are deliberately testing command
  compatibility.
- Prefer MCP functions such as `SetAppearance`, `Export`, and
  `RunPreflightChecks` when they cover the job directly.

## Safe First Tasks

- Verify Illustrator Claw can read this repo.
- Verify Illustrator Claw can list its configured tools.
- Read the repo and produce a public-only setup summary.
- List documented Illustrator MCP tools.
- Run a read-only Illustrator document inspection.
- Build a dry-run recolor plan from `workflows/illustrator-recolor.md`.
- Look up menu command values from `docs/illustrator-menu-command-links.md`.
- Run a local listener test from `workflows/mcp-listener-environment.md`.

## Troubleshooting

| Symptom | Check |
|---|---|
| Illustrator Claw can read the repo but cannot use Illustrator | Confirm the Illustrator MCP server is running and configured in private Illustrator Claw settings. |
| Tool listing works but document calls fail | Open a test Illustrator document and retry `ListDocuments`. |
| Menu command has no effect | Confirm the command is valid for your Illustrator version and that document or selection requirements are met. |
| Agent wants to paste a token into a doc | Stop the run and move the token to a private secret store. |
| Agent edits private project details into the repo | Revert that edit before committing and move the detail to a private workspace. |

## Public Boundary

This repository should only contain reusable public notes. Keep these out of
git:

- Illustrator Claw tokens, API keys, session files, logs, caches, and local databases.
- Full local MCP connection commands if they include secrets.
- Private agent names, hostnames, account names, or workspace paths.
- Client artwork, screenshots, file names, and production documents.

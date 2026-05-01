---
name: illustrator-claw
description: Public-safe Illustrator Claw setup and automation workflow for connecting an Illustrator Claw agent runner to this Illustrator MCP repository. Use when Codex needs to document, configure, or verify Illustrator Claw workspace setup; design Illustrator Claw automations; connect Illustrator Claw to Illustrator MCP tools; use the Illustrator menu command index; or keep Illustrator Claw-related repo changes free of secrets, private paths, hostnames, logs, and local runtime state.
---

# Illustrator Claw

Use this skill to make Illustrator Claw work with this public Illustrator automation
repo without leaking private setup details.

## Load References

Read only what the task needs:

- `docs/illustrator-claw-public-setup.md` for beginner connection steps.
- `docs/illustrator-claw-automation-blueprints.md` for safe automation patterns.
- `docs/public-boundary.md` before any public repo edit.
- `docs/adobe-illustrator-mcp-tools.md` for callable Illustrator MCP tools.
- `docs/illustrator-menu-command-links.md` for Illustrator menu command values.
- `data/illustrator-menu-commands.csv` when the generated menu index needs to be
  rebuilt or checked.

## Public Boundary

Keep these out of committed files and public answers:

- API keys, bearer tokens, auth files, session files, logs, caches, local
  databases, and environment files.
- Private Illustrator Claw workspace names, hostnames, gateway details, account names,
  local absolute paths, schedules, and agent logs.
- Client artwork, document names, screenshots, thumbnails, exports, and private
  production prompts.

Use placeholders such as `[private Illustrator Claw workspace]` or `[local MCP URL]`
when an example needs a value.

## Connection Workflow

1. Confirm whether the task is public documentation or live private setup.
2. For public docs, explain components and verification steps without copying
   private values.
3. For live setup, verify the actual Illustrator Claw runtime or workspace before
   trusting exported notes.
4. Confirm the repo checkout is readable by Illustrator Claw.
5. Keep MCP server URLs and bearer tokens in the user's private Illustrator Claw
   settings or secret store.
6. Verify the connected tool list before attempting document or artwork calls.
7. Test Illustrator automation on a blank or disposable document first.

## Automation Defaults

- Start with read-only inventory: list tools, list documents, inspect the active
  artboard, capture a preview, and run preflight.
- Prefer dry runs before transforms, recolors, cleanup, and exports.
- Require human approval before destructive, bulk, locked-art, hidden-art, or
  irreversible edits.
- Store generated logs, screenshots, previews, and exports outside this public
  repo unless they are fully redacted public examples.
- Prefer explicit MCP functions over menu commands when both can do the job.

## Menu Commands

When using menu command data:

1. Search `docs/illustrator-menu-command-links.md` by menu path or command
   value.
2. Use the `value` field as the command identifier.
3. Check `docRequired`, `selRequired`, `minVersion`, `maxVersion`, and `ignore`.
4. Avoid `ignore` rows unless the user is testing compatibility.
5. Rebuild the index with `python3 tools/build-menu-command-links.py` after
   changing `data/illustrator-menu-commands.csv`.

## Repo Edit Checks

Before committing Illustrator Claw-related repo changes:

```bash
git diff --check
rg -n "auth[.]json|session[_]index|state_[0-9]+[.]sqlite|logs_[0-9]+[.]sqlite|BEGIN (RSA|OPENSSH|PRIVATE) KEY" README.md CONTRIBUTING.md NOTICE.md SECURITY.md docs data tools workflows skills
```

If the menu command generator changed, also run:

```bash
python3 -m py_compile tools/build-menu-command-links.py
python3 tools/build-menu-command-links.py
```

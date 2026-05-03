---
name: illustrator-claw
description: >
  Use when automating Adobe Illustrator (Beta) tasks through an AI agent —
  including recoloring artwork, running artboard audits, checking linked
  assets, exporting, aligning objects, or looking up Illustrator menu command
  values. Also use for connecting Codex, Claude Code, or Cursor to the
  Illustrator MCP server, setting up an Illustrator Claw workspace with this
  repo, or editing this public repo without leaking credentials or private
  paths. Applies even when the user does not mention "Illustrator Claw" or
  "MCP" — use whenever someone wants an AI agent to inspect, modify, or
  automate work in Illustrator (Beta).
---

# Illustrator Claw

## Gotchas

- `SetAppearance` requires UUID values from `GetVisualAppearance`. You cannot construct or guess UUIDs — always fetch them first.
- The Illustrator MCP bearer token is session-scoped and changes each time Illustrator (Beta) restarts. Never cache it or commit it.
- `ListDocuments` returns an empty list when Illustrator has no open files. Open a test document before any document or artwork call.
- The `ignore` flag in the menu command CSV means the command crashes or silently fails, not that it is deprecated. Skip these rows unless explicitly testing compatibility.
- `RunPreflightChecks` reports linked-asset warnings for files stored outside Illustrator's expected path. This is expected in sandbox or test setups — verify manually before treating it as a blocking failure.
- Menu commands operate on the active document at call time. If the active document switches between calls, you will operate on the wrong file. Use `SwitchDocument` to pin the target before a sequence.

## Public Boundary

Never commit or paste these into any file or answer:

- API keys, bearer tokens, auth files, session files, logs, caches, local databases, `.env` files
- Private workspace names, hostnames, gateway details, account names, absolute paths, schedules, agent logs
- Client artwork, document names, screenshots, thumbnails, exports, production prompts

Use `[local MCP URL]`, `[bearer token]`, `[workspace path]` as placeholders when an example needs a value. Read `docs/public-boundary.md` before committing any change.

## Automation Sequence

For any live Illustrator task:

- [ ] 1. Call `ListDocuments`. If empty, ask the user to open a test document first.
- [ ] 2. Call `GetActiveArtboard` and `CapturePreview` — confirm you are on the right file.
- [ ] 3. Call `RunPreflightChecks` — note any issues before touching artwork.
- [ ] 4. State the planned actions. If any are destructive, bulk, or irreversible, wait for explicit approval.
- [ ] 5. Execute — prefer MCP functions over menu commands when both can do the job.
- [ ] 6. Call `CapturePreview` again and confirm the visual outcome.
- [ ] 7. Store previews, logs, and exports outside this public repo.

## Recolor Plan Pattern

Before calling `SetAppearance`:

1. Call `GetVisualAppearance` on the target objects — collect the exact UUIDs and current values.
2. Build a mapping: UUID → new fill/stroke values.
3. State the mapping for approval.
4. Call `SetAppearance` with the approved mapping only.
5. Call `CapturePreview` — verify visually and revert if the outcome is unexpected.

## Menu Commands

Load `docs/illustrator-menu-command-links.md` when the user asks for a menu command value.

1. Find the row by menu path or display name.
2. Use the `value` field as the command identifier.
3. Check `docRequired`, `selRequired`, `minVersion`, `maxVersion` before running.
4. Skip rows where `ignore` is set.

After editing `data/illustrator-menu-commands.csv`, rebuild the index:

```bash
python3 -m py_compile tools/build-menu-command-links.py
python3 tools/build-menu-command-links.py
```

## Repo Edit Checks

Run before committing:

```bash
git diff --check
rg -n "auth[.]json|session[_]index|state_[0-9]+[.]sqlite|logs_[0-9]+[.]sqlite|BEGIN (RSA|OPENSSH|PRIVATE) KEY" README.md CONTRIBUTING.md NOTICE.md SECURITY.md docs data tools workflows skills
```

## Reference Files

Load only when the task requires it:

- `docs/illustrator-claw-public-setup.md` — connection steps and private value checklist
- `docs/illustrator-claw-automation-blueprints.md` — automation patterns and prompt starters
- `docs/adobe-illustrator-mcp-tools.md` — full 43-function MCP tool reference
- `data/illustrator-menu-commands.csv` — raw menu command data (use when rebuilding the index)

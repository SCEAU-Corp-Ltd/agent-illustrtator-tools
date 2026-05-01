# Illustrator Claw Automation Blueprints

These are public automation patterns for using Illustrator Claw-style AI agents with
Illustrator MCP tools and the menu command reference data in this repo.

Keep production documents, private prompts, private endpoints, and tokens out of
the repo. Run new automations on scratch documents before using real artwork.

## Safety Defaults

- Start every automation with a read-only inventory step.
- Prefer dry runs for transforms, recolors, cleanup, and exports.
- Capture a preview before and after visual changes.
- Run preflight before export.
- Require human approval before destructive, bulk, or hidden-art edits.
- Store generated logs outside the public repository.

## Blueprint Table

| Automation | Trigger | Tool pattern | Output |
|---|---|---|---|
| Artboard health audit | Manual or scheduled | `ListDocuments` -> `GetActiveArtboard` -> `GetArtboardStructure` -> `CapturePreview` -> `RunPreflightChecks` | Short QA report with preview path and preflight issues. |
| Recolor dry run | Manual | `GetVisualAppearance` -> plan -> `SetAppearance` on scratch copy -> `CapturePreview` | Before/after preview and list of changed UUIDs. |
| Export package check | Manual or release gate | `GetLinksInformation` -> `RunPreflightChecks` -> `Export` | Exported file plus missing-link and preflight summary. |
| Object isolation | Manual | `SelectObjects` -> `VisualizeSelection` -> `GetBounds` -> `GetGeometry` | Verified target set before edits. |
| Layer naming pass | Manual | `GetCanvasStructure` -> `RenameObject` or `CreateLayer` when approved | Consistent layer/object names for handoff. |
| Layout alignment pass | Manual | `GetBounds` -> `AlignObjects` -> `DistributeObjects` -> `CapturePreview` | Clean alignment with a preview checkpoint. |
| Linked asset verifier | Manual or scheduled | `GetLinksInformation` -> report | List of linked, missing, embedded, or suspect assets. |
| Typography spot check | Manual | `GetTypographyMetrics` -> `CapturePreview` | Font, text size, and overflow notes. |
| Menu command lookup | Manual | Search `docs/illustrator-menu-command-links.md` | Command `value`, menu path, requirements, and version guard. |
| Menu command compatibility test | Manual on scratch doc | Use command `value` from CSV, then preview/preflight | Pass/fail notes by Illustrator version. |
| Listener event relay | Local test | `tools/listener-playground/listener.py` plus `send-test-event.ps1` | Local event payload received by a test listener. |
| Public doc maintenance | Manual | Read docs -> edit public notes -> run privacy checks | Updated public docs with no private data. |

## Prompt Starters

Read-only audit:

```text
Use the Illustrator MCP tools to inspect the active document. List documents,
get the active artboard, capture a preview, and run preflight checks. Do not
modify artwork.
```

Recolor plan:

```text
Read workflows/illustrator-recolor.md. Inspect the selected objects and produce
a dry-run recolor plan. Do not call SetAppearance until the plan is approved.
```

Command lookup:

```text
Find the Illustrator menu command value for the requested menu path in
docs/illustrator-menu-command-links.md. Report the command value, document or
selection requirements, version limits, and whether the row is marked ignored.
```

Export check:

```text
Check linked assets and preflight status before export. If clean, propose export
settings. Do not export until the settings are approved.
```

## Implementation Notes

- Use MCP functions before menu commands when both can do the same job.
- Use menu commands for gaps in the MCP surface, version experiments, or
  command-palette workflows.
- Keep per-project instructions in a private workspace.
- Keep public docs generic enough that another user can follow them with their
  own Illustrator Claw instance and their own Illustrator setup.

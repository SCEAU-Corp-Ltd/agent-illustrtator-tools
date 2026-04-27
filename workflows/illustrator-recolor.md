# Illustrator Recolor Workflow

Use this workflow when the user asks to recolor selected artwork, a panel, a
motif, a group, an artboard, or a saved state in Illustrator.

## Scope

This workflow is for Illustrator objects whose appearance can be changed
through the MCP appearance tools: vector fills, strokes, opacity, blend mode,
and compatible text-object appearance. It does not directly recolor embedded
raster pixels or external linked artwork.

## Required Inputs

- Target: current selection, UUIDs, layer/group name, artboard, or described
  region.
- Color intent: exact colors, palette, colorway name, or reference object.
- Output intent: live document edit only, preview, export, or placement onto a
  target page.

## Tool Sequence

1. Confirm the target document with `ListDocuments`, `SwitchDocument`, or
   `GetActiveArtboard`.
2. Identify target objects with `VisualizeSelection`, `GetCanvasStructure`,
   `GetArtboardStructure`, or `GetObjectStructure`.
3. Read current color state with `GetVisualAppearance`.
4. For placed or embedded image targets, inspect with `GetImageProperties` and
   `GetLinksInformation` before promising editable color changes.
5. Apply color changes with `SetAppearance`.
6. If text content changes are also requested, use `EditSimpleText`; keep text
   recolor in `SetAppearance`.
7. Verify visible output with `CapturePreview`.
8. Run `RunPreflightChecks` when the result is for final output or export.
9. Export with `Export` only when the user asks for a file output.

## SetAppearance Defaults

- Set `fillColor` for filled vector art.
- Set `strokeColor` for outlines, construction lines, or illustrated seams only
  when the user wants those recolored.
- Keep `strokeWeight` unchanged unless the user asks for line-weight changes.
- Keep `opacity` and `blendMode` unchanged unless the recolor needs a transparent
  overlay or multiply-style state.
- Do not set `locked=false` or `hidden=false` unless the user explicitly asks to
  unlock or show hidden artwork.

## Colorway Pattern

For multiple colors, group target UUIDs by final color, then run one
`SetAppearance` operation per color group. This keeps broad recolors auditable
and easier to undo.

Example operation plan:

| Target group | Appearance change |
|---|---|
| Main panels | new fill color |
| Trim or binding | new fill color, preserve stroke |
| Printed motif | new fill color or opacity change |
| Construction lines | unchanged unless requested |

## Verification

- Use `CapturePreview` after the recolor and inspect the result before export.
- Use `RunPreflightChecks` for final output files.
- Use `Export` with `overwrite=false` unless the user explicitly approves
  overwriting an existing file.

## Failure Modes

- If the target is a linked raster image, document that `SetAppearance` cannot
  recolor the pixels directly.
- If the structure call cannot identify stable UUIDs, ask for a selection or a
  named layer/group rather than guessing.
- If locked art blocks the change, report the locked target and wait for explicit
  permission before using force/unlock behavior.

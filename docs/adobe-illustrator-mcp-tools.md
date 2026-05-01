# Adobe Illustrator MCP Tool Snapshot

Current documented callable surface: 43 functions.

Available functions can vary by server or bridge version. Verify the active
tool list before relying on this snapshot.

This workflow depends on Adobe Illustrator (Beta). Adobe describes the MCP
server as a Beta feature for connecting desktop AI tools, including Codex, to
Illustrator (Beta).

Official Adobe references:

- [About using desktop AI tools with Adobe Illustrator (Beta)](https://helpx.adobe.com/au/illustrator/desktop/connect-with-other-apps-and-tools/about-using-ai-tools-with-illustrator.html)
- [Connect Adobe Illustrator (Beta) to AI tools](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/connect-illustrator-to-ai-tools.html)
- [Work with Adobe Illustrator (Beta) documents from AI tools](https://helpx.adobe.com/illustrator/desktop/connect-with-other-apps-and-tools/work-with-illustrator-documents-from-ai-tools.html)

## Document

| # | Function | Attributes |
|---|---|---|
| 1 | `CreateDocument` | `width`, `height`, `documentName?`, `artboardName?`, `units?`, `colorMode?`, `rasterEffectsResolution?`, `bleed?` |
| 2 | `ListDocuments` | none |
| 3 | `OpenDocument` | `filePath` |
| 4 | `SwitchDocument` | one of `index?`, `name?`, `filePath?` |

## Artboards

| # | Function | Attributes |
|---|---|---|
| 5 | `CreateArtboard` | `width`, `height`, `artboardName?`, `left?`, `top?` |
| 6 | `DeleteArtboard` | `artboardIndex?`, `artboardName?`, `removeContent?`, `force?` |
| 7 | `DuplicateArtboard` | `newLeft`, `newTop`, `artboardIndex?`, `artboardName?`, `newName?`, `duplicateContent?` |
| 8 | `FitArtboard` | `artboardIndex?`, `artboardName?`, `scope?`, `uuids?`, `force?` |
| 9 | `GetActiveArtboard` | none |
| 10 | `ListArtboards` | none |
| 11 | `MoveArtboards` | `artboardIndices`, `newLefts`, `newTops`, `moveContent?`, `force?` |
| 12 | `RenameArtboard` | `newName`, `artboardIndex?`, `artboardName?` |
| 13 | `ScaleArtboards` | `artboardIndices`, `mode`, `scaleXValues`, `scaleYValues`, `anchors?`, `scaleContent?`, `force?` |
| 14 | `SetActiveArtboard` | `artboardIndex?`, `artboardName?` |

## Structure

| # | Function | Attributes |
|---|---|---|
| 15 | `GetCanvasStructure` | `maxDepth?`, `uuids?` |
| 16 | `GetArtboardStructure` | `artboardIndex?` |
| 17 | `GetObjectStructure` | `uuids`, `maxDepth?`, `includeTypes?` |
| 18 | `VisualizeSelection` | none |

## Objects And Layers

| # | Function | Attributes |
|---|---|---|
| 19 | `CreateLayer` | `layerName`, `parentID?`, `position?` |
| 20 | `CreateGroup` | `artName?`, `parentID?`, `position?` |
| 21 | `CreateClippingMask` | `maskUuid`, `clipUuids`, `artName?`, `parentID?`, `position?` |
| 22 | `MoveObjectsToContainer` | `uuids`, `parentID?`, `position?` |
| 23 | `ArrangeArt` | `uuids`, `operation` |
| 24 | `RenameObject` | `uuids`, `newNames` |
| 25 | `DeleteObjects` | `uuids` |
| 26 | `SelectObjects` | `uuids`, `select?`, `deselectOthers?` |
| 27 | `DuplicateObjects` | `uuids`, `artName?`, `offsetX?`, `offsetY?` |

## Layout And Transform

| # | Function | Attributes |
|---|---|---|
| 28 | `AlignObjects` | `uuids`, `alignment`, `relativeTo?` |
| 29 | `DistributeObjects` | `uuids`, `axis`, `spacing?` |
| 30 | `MoveObjects` | `uuids`, `x`, `y`, `mode?` |
| 31 | `RotateObjects` | `uuids`, `angle` |
| 32 | `ScaleObjects` | `uuids`, `sx`, `sy`, `mode?` |
| 33 | `GetBounds` | `uuids` |
| 34 | `GetGeometry` | `uuids` |

## Appearance, Text, Assets, And QA

| # | Function | Attributes |
|---|---|---|
| 35 | `SetAppearance` | `uuids`, `fillColor?`, `strokeColor?`, `strokeWeight?`, `strokeDash?`, `strokeCap?`, `strokeJoin?`, `opacity?`, `blendMode?`, `locked?`, `hidden?` |
| 36 | `GetVisualAppearance` | `uuids` |
| 37 | `EditSimpleText` | `uuid`, `text` |
| 38 | `GetTypographyMetrics` | `uuids` |
| 39 | `GetImageProperties` | `uuids` |
| 40 | `GetLinksInformation` | `uuids` |
| 41 | `RunPreflightChecks` | `artboardIndex?` |
| 42 | `CapturePreview` | `reason`, `targetType?`, `artboardIndex?`, `uuids?`, `width?`, `height?`, `cropX?`, `cropY?`, `cropWidth?`, `cropHeight?` |
| 43 | `Export` | `format`, `targetType?`, `outputMode?`, `outputPath?`, `artboardIndex?`, `uuids?`, `resolution?`, `quality?`, `overwrite?` |

## Recolor Tool Use

Use tools 35-43 as an implementation sequence, not as isolated commands:

1. `GetVisualAppearance` reads the current fill, stroke, opacity, blend mode,
   and lock/hidden state for target UUIDs.
2. `SetAppearance` applies the actual recolor: fill, stroke, stroke weight,
   opacity, blend mode, or visibility/lock changes when explicitly requested.
3. `EditSimpleText` is only for text content changes. Text color should still
   be handled through appearance when the MCP supports the text object.
4. `GetImageProperties` and `GetLinksInformation` distinguish editable vector
   art from placed/raster assets. Do not promise direct raster recolor through
   `SetAppearance`.
5. `RunPreflightChecks`, `CapturePreview`, and `Export` verify and deliver the
   recolored result.

The practical workflow lives in `workflows/illustrator-recolor.md`.

## Menu Commands

Some Illustrator actions may not have a dedicated MCP function. For those gaps,
use `docs/illustrator-menu-command-links.md` as a public command-value
reference and verify version, document, and selection requirements before
running a command.

### macOS Menu Command Bridge

On macOS, `app.executeMenuCommand()` can be called through AppleScript even
when the MCP server does not expose an `ExecuteMenuCommand` tool:

```bash
osascript -e 'tell application "Adobe Illustrator" to do javascript "app.executeMenuCommand(\"enterFocus\")"'
```

This bridges the gap between the 43-tool MCP surface and the full 786-command
menu reference. Any command value from `docs/illustrator-menu-command-links.md`
can be executed this way. Common examples:

| Command value | Menu path | Use case |
|---|---|---|
| `enterFocus` | Other Object > Isolate Selected Object | Access symbol internals |
| `exitFocus` | Other Object > Exit Isolation Mode | Return to document root |
| `Recolor Art Dialog` | Edit > Edit Colors > Recolor Artwork... | Opens recolor dialog |
| `Expand3` | Object > Expand... | Expand selected objects |
| `expandStyle` | Object > Expand Appearance | Expand appearance attributes |
| `undo` | Edit > Undo | Undo last action |
| `selectall` | Edit > Select All | Select all at current level |

`executeMenuCommand` returns `undefined`; success or failure must be verified
by inspecting document state afterward.

### Symbol Internals via Isolation Mode

`GetObjectStructure` treats symbol instances as opaque — no children are
returned. `breakLink()` unpacks only the top level of the symbol definition,
which may contain only overlay elements (logos, detail lines) while body
content remains inside nested structures.

To access all content inside a symbol:

1. Select the symbol instance (`SelectObjects`).
2. Execute `enterFocus` to enter isolation mode.
3. Use `selectall` and ExtendScript to enumerate all paths at that level.
4. Execute `enterFocus` again to drill into nested groups or sub-symbols.
5. Repeat until the target paths are found.
6. Modify paths as needed (recolor, transform).
7. Execute `exitFocus` to return up one level; repeat until back at the
   document root.

**MCP limitation:** The 43-tool MCP server refuses all calls while in
isolation mode and returns an error asking the user to exit first. Use
ExtendScript via the AppleScript bridge (macOS) or `ExecuteMenuCommand` (when
available) to operate inside isolation mode.

## Attribute Notes

- `?` means optional.
- `uuids` is always an array, even when passing one object.
- Artboard indices are zero-based.
- Canvas coordinates are in points, with Y increasing downward.
- `force` should only be used when the user explicitly asks to affect locked
  artboards.
- `locked=false` and `hidden=false` should only be used when the user explicitly
  asks to unlock or show hidden artwork.

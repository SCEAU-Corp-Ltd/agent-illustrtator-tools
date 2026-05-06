# Design QA With Ollama Vision

Optional loop for **local, offline visual review** of Illustrator MCP exports.
Use this after `CapturePreview`, `Export`, or any step that produces a PNG you
can read from disk.

This complements human review and cloud-model vision: nothing leaves your
machine except HTTP to your local Ollama process.

## When To Use It

- Sanity-check recolor or layout after MCP changes.
- Compare before/after PNGs with one prompt (`--image` twice).
- Produce a short written checklist for logs or handoff (no secrets in prompts).

## Prerequisites

1. [Ollama](https://ollama.com) installed and running (`ollama serve` or the desktop app).
2. A **vision-capable** model pulled, for example:

   ```bash
   ollama pull llava
   # alternatives: qwen2-vl, gemma3, minicpm-v — use `ollama list` for exact tags
   ```

   For **Qwen VL vs Gemma 3** pull commands, sizes, and env presets, use
   [`ollama-qwen-gemma-vision.md`](ollama-qwen-gemma-vision.md).

3. Python **3.9+** (stdlib only — no `pip install` for this helper).

Optional: copy [`.env.example`](../.env.example) into a **local** env file and set
`OLLAMA_MODEL`, `OLLAMA_BASE_URL` if you do not use defaults.

## Workflow

1. **Produce a PNG** via Illustrator MCP (`CapturePreview`, `Export`, or your client’s
   stream-to-file path). Save it outside this repo if it contains private artwork
   ([`docs/public-boundary.md`](../docs/public-boundary.md)).
2. **Run the helper** from the repository root:

   ```bash
   export OLLAMA_MODEL=llava   # or your pulled vision tag

   python3 tools/ollama-vision/ollama_vision.py \
     --prompt "List dominant fills and strokes. Note misaligned panels, clipped masks, or unreadable text. Be concise." \
     --image ./preview-after-recolor.png
   ```

3. **Iterate in Illustrator** based on the model output; export again and repeat.

### Before / After

```bash
python3 tools/ollama-vision/ollama_vision.py \
  -p "Compare A vs B: what changed in color and geometry? Any regressions?" \
  -i ./before.png \
  -i ./after.png
```

### Base64 From Automation

If your pipeline already has raw base64 (for example from an MCP `Export` stream),
pass it directly:

```bash
python3 tools/ollama-vision/ollama_vision.py \
  -p "Describe colors and layout for QA." \
  --image-base64 "$PNG_BASE64"
```

## Combine With Recolor

Use [`illustrator-recolor.md`](illustrator-recolor.md) for MCP steps, then run this
document’s steps **after** verification/export whenever you want a second opinion
from a local vision model.

## Troubleshooting

| Symptom | Likely fix |
|--------|------------|
| Connection refused | Start Ollama; confirm `OLLAMA_BASE_URL` (default `http://127.0.0.1:11434`). |
| Model not found | `ollama pull <tag>` matching `OLLAMA_MODEL`. |
| Nonsense answers | Try another vision tag (`qwen2-vl`, `llava`); tighten the prompt. |

See [`tools/ollama-vision/README.md`](../tools/ollama-vision/README.md) for API details.

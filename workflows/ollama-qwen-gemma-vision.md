# Ollama: Qwen or Gemma vision workflow

Use this when you want **local multimodal QA** with **Qwen VL** or **Gemma 3** instead of the generic `llava` default. The same helper and loop as [`design-qa-with-ollama.md`](design-qa-with-ollama.md) apply; this page is only **model choice, pull commands, and env presets**.

Upstream catalogs (verify tags before pulling): [qwen2.5vl](https://ollama.com/library/qwen2.5vl), [qwen2-vl](https://ollama.com/search?q=qwen2-vl), [gemma3](https://ollama.com/library/gemma3).

## Choose a path

| Goal | Suggested starting tag | Rough size (Ollama registry) |
| --- | --- | --- |
| Strong vision + reasoning, default “Qwen” path | `qwen2.5vl:7b` or `qwen2.5vl:3b` | ~6 GB / ~3.2 GB |
| Prefer Google Gemma, single-GPU friendly | `gemma3:4b` | ~3.3 GB |
| More capacity if VRAM allows | `qwen2.5vl:32b`, `gemma3:12b`, `gemma3:27b` | See library pages |

**Gemma caveat:** only tags that list **Text, Image** input are vision-capable (for example `gemma3:4b`, `gemma3:12b`). Smaller tags such as `gemma3:270m` / `gemma3:1b` are **text-only** in the registry.

**Older Qwen:** `qwen2-vl` remains in the library; if you already use it, keep `OLLAMA_MODEL` aligned with `ollama list`.

## Setup

1. Install and run [Ollama](https://ollama.com) (keep it updated; newer VL models expect recent clients).
2. Pull **one** vision tag (examples):

   ```bash
   # Qwen 2.5 VL (recommended Qwen path on Ollama)
   ollama pull qwen2.5vl:7b

   # Gemma 3 vision (light local default)
   ollama pull gemma3:4b
   ```

3. Point the helper at that tag:

   ```bash
   export OLLAMA_MODEL=qwen2.5vl:7b
   # or
   export OLLAMA_MODEL=gemma3:4b
   ```

   Optionally copy [`.env.example`](../.env.example) into a **local** env file (not committed) and set `OLLAMA_MODEL` there.

## Workflow (same as generic design QA)

1. Export or save a PNG from Illustrator MCP (or decode a stream to a file). Keep private artwork out of this repo ([`docs/public-boundary.md`](../docs/public-boundary.md)).
2. From the repository root:

   ```bash
   python3 tools/ollama-vision/ollama_vision.py \
     -m "${OLLAMA_MODEL}" \
     -p "List dominant colors and flat fills. Flag misalignment, clipped masks, unreadable text, and accidental overlaps. Be concise." \
     -i ./preview.png
   ```

3. Iterate in Illustrator; re-export and rerun as needed.

**Before/after:**

```bash
python3 tools/ollama-vision/ollama_vision.py \
  -m "${OLLAMA_MODEL}" \
  -p "Compare A vs B: color and geometry changes; any regressions?" \
  -i ./before.png \
  -i ./after.png
```

**Automation with base64** (for example MCP `Export` stream): see [`design-qa-with-ollama.md`](design-qa-with-ollama.md#base64-from-automation).

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `model ... not found` | `ollama list` — tag must match `OLLAMA_MODEL` exactly (`qwen2.5vl:7b` ≠ `qwen2.5-vl:7b`). |
| Slow or OOM | Try `qwen2.5vl:3b` or `gemma3:4b`; close other GPU workloads. |
| Weak layout answers | Tighten the prompt; try the larger tag in the same family; ensure image resolution is readable (not tiny thumbs). |

For API and library usage, see [`tools/ollama-vision/README.md`](../tools/ollama-vision/README.md). For the full optional QA loop narrative, see [`design-qa-with-ollama.md`](design-qa-with-ollama.md).

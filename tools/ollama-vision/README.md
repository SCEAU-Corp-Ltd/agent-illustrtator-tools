# Ollama vision helper

Small stdlib Python helper for **local multimodal chat** against Ollama's `POST /api/chat` endpoint (same shape as Adobe / agent workflows that export preview PNGs and want a text description).

## Setup

1. Install and run [Ollama](https://ollama.com).
2. Pull a vision-capable tag, for example:

   ```bash
   ollama pull llava
   # alternatives: qwen2.5vl, qwen2-vl, gemma3 (vision tags), minicpm-v
   ```

   Use whatever tag `ollama list` shows; set `OLLAMA_MODEL` to match.

   **Qwen or Gemma:** see [`workflows/ollama-qwen-gemma-vision.md`](../../workflows/ollama-qwen-gemma-vision.md) for recommended tags (`qwen2.5vl:7b`, `gemma3:4b`, etc.) and a full loop.

## Environment

| Variable | Purpose |
|----------|---------|
| `OLLAMA_BASE_URL` | API base (default `http://127.0.0.1:11434`) |
| `OLLAMA_HOST` | Used if `OLLAMA_BASE_URL` is unset |
| `OLLAMA_MODEL` | Default model tag (default `llava`) |

## CLI

From the repository root:

```bash
python3 tools/ollama-vision/ollama_vision.py \
  --prompt "What colors should we recolor first?" \
  --image ./preview.png
```

Multiple images:

```bash
python3 tools/ollama-vision/ollama_vision.py -p "Compare these." -i ./a.png -i ./b.png
```

## Library

```python
from pathlib import Path
import sys
sys.path.insert(0, "tools/ollama-vision")
from ollama_vision import describe_image, vision_chat

print(describe_image(Path("preview.png")))
print(vision_chat("Any CMYK vs RGB hints?", images=["shot.png"], model="qwen2-vl"))
```

`describe_image` uses a default prompt tuned for automation / design context; override with `prompt=`.

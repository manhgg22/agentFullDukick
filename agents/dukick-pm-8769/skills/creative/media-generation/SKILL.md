---
name: media-generation
description: AI-powered media generation — images, videos, and audio — via fal.ai, Hermes Web UI endpoints (apikey-image-gen, grok-image-to-video), and other providers. Covers text-to-image, image-to-image, image-to-video, text-to-speech, and video-to-audio with cost estimation and model selection guidance.
category: creative
---

# Media Generation

Generate images, videos, and audio using AI providers. Covers fal.ai MCP, Hermes Web UI media endpoints, and related workflows.

## When to Activate

- User wants to generate images from text prompts or reference images
- Creating videos from text or images (including image-to-video animation)
- Generating speech, music, or sound effects
- Editing existing images (inpainting, outpainting, style transfer)
- Any media generation task
- User says "generate image", "create video", "text to speech", "make a thumbnail", or similar

---

## Provider A: fal.ai (via MCP)

The fal.ai MCP provides tools: `search`, `find`, `generate`, `result`, `status`, `cancel`, `estimate_cost`, `models`, `upload`.

### MCP Configuration

Add to `~/.claude.json`:

```json
"fal-ai": {
  "command": "npx",
  "args": ["-y", "fal-ai-mcp-server"],
  "env": { "FAL_KEY": "YOUR_FAL_KEY_HERE" }
}
```

### Image Generation

**Nano Banana 2 (Fast)** — quick iterations, drafts:
```
generate(
  model_name: "fal-ai/nano-banana-2",
  input: {
    "prompt": "a futuristic cityscape at sunset, cyberpunk style",
    "image_size": "landscape_16_9",
    "num_images": 1,
    "seed": 42
  }
)
```

**Nano Banana Pro (High Fidelity)** — production images:
```
generate(
  model_name: "fal-ai/nano-banana-pro",
  input: {
    "prompt": "professional product photo...",
    "image_size": "square",
    "guidance_scale": 7.5
  }
)
```

### Video Generation

**Seedance 1.0 Pro** — text/image-to-video with high motion quality:
```
generate(
  model_name: "fal-ai/seedance-1-0-pro",
  input: {
    "prompt": "drone flyover of a mountain lake...",
    "duration": "5s",
    "aspect_ratio": "16:9"
  }
)
```

**Kling Video v3 Pro** — native audio generation:
```
generate(
  model_name: "fal-ai/kling-video/v3/pro",
  input: { "prompt": "ocean waves crashing...", "duration": "5s" }
)
```

**Veo 3** — video with generated sound:
```
generate(
  model_name: "fal-ai/veo-3",
  input: { "prompt": "bustling Tokyo street market at night..." }
)
```

### Audio Generation

**CSM-1B** — conversational speech:
```
generate(
  model_name: "fal-ai/csm-1b",
  input: { "text": "Hello, welcome to the demo...", "speaker_id": 0 }
)
```

**ThinkSound** — video-to-audio:
```
generate(
  model_name: "fal-ai/thinksound",
  input: { "video_url": "<url>", "prompt": "ambient forest sounds" }
)
```

### Tips

- Use `seed` for reproducible iterations
- Start with lower-cost models for prompt exploration, switch to Pro for finals
- Check `estimate_cost` before expensive video generations

---

## Provider B: Hermes Web UI Endpoints

### apikey-image-gen — Image Generation via fun-codex

Use when generating or editing images through Hermes Web UI.

**Endpoint:**
```bash
POST <Hermes Web UI base URL>/api/hermes/media/apikey-image-generate
```

**Modes:**
- `text` — text-to-image
- `image` — image-to-image (reference-based)
- `edit` — image editing (inpainting/outpainting)

**Auth:** Hermes Web UI bearer token (not fun-codex API key directly).
**Profile:** Send `X-Hermes-Profile` header.

See `references/apikey-image-gen.md` for full curl template and field reference.

### grok-image-to-video — Image Animation via xAI

Use when animating a local image into a short MP4 with xAI Grok Imagine.

**Endpoint:**
```bash
POST <Hermes Web UI base URL>/api/hermes/media/grok-image-to-video
```

**Required:** `image_path`, `prompt`
**Optional:** `duration` (1-15s, default 8), `output_path`, `timeout_ms`

**Auth:** Hermes Web UI bearer token.
**Error:** If response has `code: "missing_xai_token"`, tell user to set `XAI_API_KEY`.

See `references/grok-image-to-video.md` for full curl template.

---

## Cost Estimation

Before generating expensive media:
1. Use fal.ai `estimate_cost(model_name, input)`
2. For Hermes endpoints, there is no built-in cost estimate — warn user before large generations

## Model Discovery

```
search(query: "text to video")    # fal.ai
find(model_name: "fal-ai/seedance-1-0-pro")
models()                          # list popular models
```

## References
- `references/apikey-image-gen.md` — Full Hermes Web UI image generation curl template
- `references/grok-image-to-video.md` — Full Hermes Web UI image-to-video curl template

---
name: hermes-media-generation
description: Generate images and videos through Hermes Web UI media endpoints using profile-configured providers (fun-codex, xAI Grok). Covers text-to-image, image-to-image, image editing, and image-to-video workflows.
---

# Hermes Media Generation

Class-level skill for generating media (images and short videos) via Hermes Web UI endpoints. The server reads the active profile's `config.yaml` to resolve providers, credentials, and tokens — agents never handle API keys directly.

## When to use

- Generate an image from a text prompt
- Generate a new image based on a reference image
- Edit an existing image (inpainting, style transfer, background swap)
- Animate a static image into a short MP4 video

## Prerequisites

- Hermes Web UI running and reachable
- Bearer token accessible (see Authentication section)
- For image generation: `fun-codex` provider configured in the active profile's `config.yaml`
- For video generation: xAI credentials configured (OAuth or `XAI_API_KEY`)

## Authentication

Resolve the Hermes Web UI base URL in this order:
1. `HERMES_WEB_UI_URL` environment variable
2. `http://127.0.0.1:${PORT}`
3. `http://127.0.0.1:8648`
4. Docker Compose default: `http://127.0.0.1:6060`

Resolve the bearer token in this order:
1. `AUTH_TOKEN` environment variable
2. `${HERMES_WEB_UI_HOME}/.token`
3. `${HERMES_WEBUI_STATE_DIR}/.token`
4. `~/.hermes-web-ui/.token`

Profile selection: send `X-Hermes-Profile` header with the exact profile name from run instructions.

## Image Generation

Endpoint: `POST <base_url>/api/hermes/media/apikey-image-generate`

### Modes

| Mode | When to use | Required fields |
|------|-------------|-----------------|
| `text` | No input image; generate from prompt only | `mode`, `prompt` |
| `image` | Reference image → new image | `mode`, `prompt`, `image_path` |
| `edit` | Modify existing image preserving parts | `mode`, `prompt`, `image_path` |

### Common request fields
- `mode`: `text`, `image`, or `edit`
- `prompt`: description of desired output
- `image_path`: local png/jpeg/webp path (required for `image` and `edit`)
- `size`: defaults to `1024x1024`. Common: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `3840x2160`, `2160x3840`, `auto`
- `quality`: defaults to `auto`
- `n`: number of images (default `1`)
- `model`: optional override. Text/edit default to `gpt-image-2`
- `output_path`: absolute path for saved output
- `timeout_ms`: defaults to `600000`

### Curl template
```bash
TOKEN="${AUTH_TOKEN:-}"
if [ -z "$TOKEN" ] && [ -f "$HOME/.hermes-web-ui/.token" ]; then
  TOKEN="$(cat "$HOME/.hermes-web-ui/.token")"
fi
if [ -z "$TOKEN" ]; then
  echo "Missing Hermes Web UI token." >&2; exit 1
fi

BASE_URL="${HERMES_WEB_UI_URL:-http://127.0.0.1:${PORT:-8648}}"
BASE_URL="${BASE_URL%/}"

curl -sS -X POST "$BASE_URL/api/hermes/media/apikey-image-generate" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "mode": "text",
    "prompt": "A cinematic 4K photo of a silver robot hand holding a small glowing cube",
    "size": "3840x2160",
    "output_path": "/absolute/path/to/output.png"
  }'
```

If response code is `missing_fun_codex_provider`, tell the user to configure `fun-codex` in the active profile's `config.yaml`.

## Image-to-Video (Grok)

Endpoint: `POST <base_url>/api/hermes/media/grok-image-to-video`

Required fields:
- `image_path`: local png/jpeg/webp
- `prompt`: motion and style instructions

Optional fields:
- `duration`: 1–15 seconds (default `8`)
- `output_path`: local save path
- `timeout_ms`: default `600000`

### Curl template
```bash
# Resolve TOKEN and BASE_URL as above

curl -sS -X POST "$BASE_URL/api/hermes/media/grok-image-to-video" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_path": "/absolute/path/to/input.png",
    "prompt": "Animate the subject with a slow cinematic push-in and subtle natural motion.",
    "duration": 8,
    "output_path": "/absolute/path/to/output.mp4"
  }'
```

If response code is `missing_xai_token`, tell the user to set `XAI_API_KEY` or complete xAI OAuth login in Hermes Web UI.

## Provider configuration

`config.yaml` custom_providers entry:
```yaml
custom_providers:
  - name: fun-codex
    base_url: https://api.apikey.fun/v1
    api_key: ...
    model: gpt-5.5
    api_mode: codex_responses
```

## Pitfalls

- Do not call `api.apikey.fun` directly — always route through the Hermes Web UI endpoint.
- Do not use built-in image/video generation tools as fallback; if the endpoint returns `401`, `403`, or connection failure, report the Hermes Web UI error and stop.
- Never send placeholder values like `<name>` in the `X-Hermes-Profile` header.
- Image mode (`mode: image`) calls `POST /v1/responses` on the fun-codex base URL; text/edit call `/v1/images/generations` and `/v1/images/edits` respectively.
- Always use absolute paths for `image_path` and `output_path`.

## Related skills

- `fal-ai-media` — for media generation via fal.ai MCP (broader model selection, independent of Hermes Web UI)
- `video-editing` — for editing real footage after generation
- `remotion` / `hyperframes` — for code-based video composition

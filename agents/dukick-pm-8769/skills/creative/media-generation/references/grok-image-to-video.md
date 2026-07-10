# Grok Image-to-Video (Hermes Web UI)

Endpoint:
```bash
POST <Hermes Web UI base URL>/api/hermes/media/grok-image-to-video
```

Resolve base URL and token exactly as in `references/apikey-image-gen.md`.

Required fields:
- `image_path`: local png/jpeg/webp
- `prompt`: motion and style instructions

Optional:
- `duration`: 1-15 seconds (default 8)
- `output_path`: local path for MP4
- `timeout_ms`: default 600000

## Curl Template

```bash
TOKEN="${AUTH_TOKEN:-}"
# ... same token resolution as apikey-image-gen ...

BASE_URL="${HERMES_WEB_UI_URL:-http://127.0.0.1:${PORT:-8648}}"
BASE_URL="${BASE_URL%/}"

curl -sS -X POST "$BASE_URL/api/hermes/media/grok-image-to-video" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_path": "/abs/path.png",
    "prompt": "Animate with a slow cinematic push-in...",
    "duration": 8,
    "output_path": "/abs/output.mp4"
  }'
```

Error `missing_xai_token`: tell user to set `XAI_API_KEY` or complete xAI OAuth login in Hermes Web UI.

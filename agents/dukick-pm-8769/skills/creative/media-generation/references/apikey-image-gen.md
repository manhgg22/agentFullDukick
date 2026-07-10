# APIKEY Image Generation (Hermes Web UI)

Endpoint:
```bash
POST <Hermes Web UI base URL>/api/hermes/media/apikey-image-generate
```

Resolve base URL:
1. `HERMES_WEB_UI_URL` env var
2. `http://127.0.0.1:${PORT}` if PORT set
3. `http://127.0.0.1:8648` (local dev)
4. `http://127.0.0.1:6060` (Docker Compose default external)

Resolve token:
1. `AUTH_TOKEN` env var
2. `${HERMES_WEB_UI_HOME}/.token`
3. `${HERMES_WEBUI_STATE_DIR}/.token`
4. `~/.hermes-web-ui/.token`

Profile header: `X-Hermes-Profile: <name>` from run instructions.

## Modes

### Text To Image
```json
{ "mode": "text", "prompt": "...", "size": "1024x1024", "output_path": "/abs/path.png" }
```

### Image To Image
```json
{ "mode": "image", "prompt": "...", "image_path": "/abs/ref.png", "size": "1024x1024" }
```

### Image Edit
```json
{ "mode": "edit", "prompt": "...", "image_path": "/abs/src.png", "size": "1024x1024" }
```

## Curl Template

```bash
TOKEN="${AUTH_TOKEN:-}"
if [ -z "$TOKEN" ] && [ -n "${HERMES_WEB_UI_HOME:-}" ] && [ -f "$HERMES_WEB_UI_HOME/.token" ]; then
  TOKEN="$(cat "$HERMES_WEB_UI_HOME/.token")"
fi
if [ -z "$TOKEN" ] && [ -n "${HERMES_WEBUI_STATE_DIR:-}" ] && [ -f "$HERMES_WEBUI_STATE_DIR/.token" ]; then
  TOKEN="$(cat "$HERMES_WEBUI_STATE_DIR/.token")"
fi
if [ -z "$TOKEN" ] && [ -f "$HOME/.hermes-web-ui/.token" ]; then
  TOKEN="$(cat "$HOME/.hermes-web-ui/.token")"
fi
if [ -z "$TOKEN" ]; then
  echo "Missing Hermes Web UI token" >&2; exit 1
fi

BASE_URL="${HERMES_WEB_UI_URL:-http://127.0.0.1:${PORT:-8648}}"
BASE_URL="${BASE_URL%/}"

curl -sS -X POST "$BASE_URL/api/hermes/media/apikey-image-generate" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"text","prompt":"...","size":"1024x1024","output_path":"/abs/path.png"}'
```

Success: `{ "ok": true, "output_paths": [...], "provider": "fun-codex" }`
Error `missing_fun_codex_provider`: tell user to configure `fun-codex` in profile `config.yaml`.

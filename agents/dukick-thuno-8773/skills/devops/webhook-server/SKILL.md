---
name: webhook-server
description: Dukick local webhook server chạy tại máy Windows (port 8080) để nhận payload từ các dịch vụ bên ngoài.
title: Dukick Webhook Server
trigger:
  - "webhook"
  - "start webhook"
  - "stop webhook"
  - "webhook server"
  - "webhook logs"
---

# Dukick Webhook Server

Chạy tại máy local (coi như server) để nhận các webhook từ bên ngoài: Stripe, Notion, Zapier, n8n, v.v.

## Port

- **8889** (đã verify không trùng — `netstat -ano | grep "8889"`)

## Files

- `scripts/webhook_server.py` — Flask server (đang chạy tại `localhost:8889`)
- `debt_data/webhook_logs.jsonl` — log tất cả payload đến

## Endpoints

| Route | Method | Mô tả |
|-------|--------|-------|
| `GET /` | GET | Health check + info |
| `GET /health` | GET | Status OK |
| `POST /webhook/zalo` | POST | Zalo Bot Platform webhook (auto-reply bot) |
| `POST /webhook/<source>` | POST/GET | Generic webhook, log lại |
| `POST /webhook/debt/update` | POST | Cập nhật trạng thái công nợ từ bên ngoài |

### Zalo Bot Webhook

**URL:** `https://<domain>/webhook/zalo`

**Headers:** `X-Bot-Api-Secret-Token: <secret_token>`

**Payload:**
```json
{
  "ok": true,
  "result": {
    "event_name": "message.text.received",
    "message": {
      "from": {"id": "...", "display_name": "..."},
      "chat": {"id": "...", "chat_type": "PRIVATE"},
      "text": "...",
      "message_id": "...",
      "date": 1234567890
    }
  }
}
```

> **Pitfall:** Zalo wraps payload in `{"ok": true, "result": {...}}`. Access via `data.get("result", data)`.

See `zalo-bot-integration` skill for full setup + auto-reply logic.

**AI Agent Integration:** See `zalo-bot-integration/references/ai-agent-integration.md` for extending the webhook server with AI (GPT-4o-mini) using real-time data context from JSON files. Key pattern: inject file-based context into the AI system prompt before calling the API.

### Payload /webhook/debt/update

```json
{
  "id": "debt-001",
  "status": "paid",
  "notes": "Đã nhận chuyển khoản"
}
```

## Kết nối ngoài (Zalo, Stripe, v.v.)

### Tailscale Funnel (khuyến nghị cho URL cố định)

Exposes port ra internet qua Tailscale — URL không đổi khi restart.

```bash
# ⚠️ MSYS path conversion pitfall!
# Trên git-bash/MSYS, --set-path=/webhook bị convert thành C:/Program Files/Git/webhook
# Fix: export MSYS_NO_PATHCONV=1 trước mọi lệnh tailscale serve/funnel

export MSYS_NO_PATHCONV=1

# Expose port 8889 ra internet với path /
tailscale funnel --bg http://127.0.0.1:8889

# Verify URL public
curl -s https://<machine>.tailc0eb7b.ts.net/health
```

**Machine name:** `admin-pc-1` → URL: `https://admin-pc-1.tailc0eb7b.ts.net/`

**Pitfall:** Tailscale Funnel forward `/webhook` → port 8889, nên request đến `https://domain/webhook/zalo` sẽ proxy thành `http://localhost:8889/webhook/zalo`. Path không bị cắt khi dùng `funnel` với root `/`.

## Start / Stop / Restart (Windows)

```bash
# Kiểm tra port trước khi start
netstat -ano | grep "8889" | grep "LISTENING"

# Start (foreground)
python scripts/webhook_server.py

# Start background
terminal background: python scripts/webhook_server.py
```

### Kill process trên Windows (cẩn thận)

`taskkill /F /IM python.exe` và `kill -9 PID` đôi khi **không chết** process trên Windows (process giữ port vẫn còn).

**Pitfall:** Sau `taskkill`, `netstat` vẫn thấy port LISTENING.

**Fix đáng tin cậy nhất — PowerShell:**

```bash
# Lấy PID từ port
tasklist | grep python
# hoặc: netstat -ano | grep "8889" | grep "LISTENING"

# Kill bằng PowerShell (always works)
powershell -Command "Stop-Process -Id <PID> -Force"
# hoặc kill toàn bộ python tree
powershell -Command "Stop-Process -Name python -Force"

# Verify port free
netstat -ano | grep "8889" | grep "LISTENING" || echo "Port free"
```

**Why:** Windows Console processes có thể spawn child processes mà `taskkill /F /PID` không bắt được. PowerShell `Stop-Process -Force` kills cả process tree.

### Restart đúng cách (không bị zombie process)

```bash
# Step 1: Kill đúng
powershell -Command "Stop-Process -Name python -Force"
sleep 2

# Step 2: Verify port free
netstat -ano | grep "8889" | grep "LISTENING" || echo "Port free"

# Step 3: Start lại
python scripts/webhook_server.py

# Step 4: Verify health
curl http://localhost:8889/health
```

### Kiểm tra đang chạy không

```bash
curl http://localhost:8889/health
curl http://localhost:8889/
```

---
name: zalo-bot-integration
description: Kết nối Dukick webhook server với Zalo Bot Platform — nhận tin nhắn, auto-reply công nợ, gửi thông báo qua Zalo OA.
title: Zalo Bot Integration for Dukick
trigger:
  - "zalo bot"
  - "zalo webhook"
  - "zalo OA"
  - "kết nối zalo"
  - "zalo config"
---

# Zalo Bot Integration — Dukick

## Overview

Dukick webhook server đã tích hợp Zalo Bot Platform. User nhắn tin vào OA → server nhận webhook → auto-reply (tổng quan công nợ, chi tiết, help).

## Zalo Bot Platform vs Zalo OA Platform

| | Zalo Bot Platform | Zalo OA Platform |
|---|---|---|
| Console | bot.zaloplatforms.com | oa.zalo.me |
| Token field | **Bot Token** | OA Access Token |
| API reply | `POST https://bot-api.zaloplatforms.com/bot{BOT_TOKEN}/sendMessage` | `POST https://openapi.zalo.me/v2.0/oa/message` |
| Webhook event | `message.text.received` | `user_send_text` |
| Payload | `{"ok": true, "result": {"message": {...}}}` | `{"sender": {...}, "message": {...}}` |

**Pitfall:** Dùng Zalo OA API (`openapi.zalo.me`) với Bot Token → im lặng, không reply.
**Fix:** Dùng đúng API endpoint: `bot-api.zaloplatforms.com/bot{BOT_TOKEN}/sendMessage`

Xem chi tiết docs đã crawl trong `references/zalo-api-docs.md`.

- `scripts/webhook_server.py` — Flask server có endpoint `/webhook/zalo`
- `debt_data/zalo_config.json` — OA token, `secret_token`, app_id, secret_key
- `debt_data/zalo_webhook_url.txt` — URL public hiện tại

## Webhook URL (Public — CỐ ĐỊNH qua Tailscale Funnel)

**`https://admin-pc-1.tailc0eb7b.ts.net/webhook/zalo`**

> ✅ URL này **KHÔNG đổi** khi restart. Dùng Tailscale Funnel expose port 8888 ra internet.
> > Machine: `admin-pc-1` | Tailnet IP: `100.90.204.49`

## Setup Steps

### 1. Đăng ký Zalo Bot
- Vào https://bot.zalo.me → tạo Bot
- Lấy **Bot Token** (format: `<oa_id>:<long_random_string>`)

### 2. Cấu hình token

Edit `debt_data/zalo_config.json`:

```json
{
  "bot_token": "<oa_id>:<long_random_string>",
  "secret_token": "<32-64_hex_chars>",
  "app_id": "YOUR_APP_ID",
  "secret_key": "YOUR_SECRET_KEY",
  "oa_id": "YOUR_OA_ID"
}
```

> **bot_token** = **Bot Token** từ Zalo console (format `oa_id:long_string`). Không phải OA access token.
> **secret_token** = tự generate 32-64 hex chars, paste vào cả Zalo console lẫn server config.

## Verify Token After Edit

Hermes masks tokens with `***` in file reads. Dùng Python để verify:

```python
import json
with open("zalo_config.json", "r") as f:
    cfg = json.load(f)
print(f"bot_token length: {len(cfg['bot_token'])}")
print(f"ends with: ...{cfg['bot_token'][-20:]}")
```

## Restart Server — Windows Pitfall

```bash
# taskkill đôi khi không kill được process python
taskkill /F /IM python.exe /T 2>/dev/null; sleep 2

# Nếu vẫn còn → dùng PowerShell
powershell -Command "Stop-Process -Name python -Force"

# Verify port free
netstat -ano | grep "8888" | grep "LISTENING" || echo "Port free"

# Start lại
python scripts/webhook_server.py
```

### 3. Cấu hình Webhook trong Zalo Console

Console Zalo Bot (mobile/web) chỉ có **3 fields**:

| Field | Giá trị |
|-------|---------|
| **Webhook URL** | `https://<your-domain>/webhook/zalo` — **phải có path đầy đủ** `/webhook/zalo`, không chỉ domain |
| **Secret Token** | Paste secret_token đã generate |
| **Bot Token** | Copy từ console, paste vào `zalo_config.json` → **`bot_token`** |

**Pitfall:** URL thiếu path → webhook vẫn verify OK nhưng Zalo không POST event.

Bấm **"Lưu thay đổi"** ✅

### 4. Restart server để load token mới

```bash
# Kill python server (Windows pitfall: taskkill đôi khi không chết)
powershell -Command "Stop-Process -Name python -Force"

# Verify port free
netstat -ano | grep "8888" | grep "LISTENING" || echo "Port free"

# Start lại
python scripts/webhook_server.py
```

### 5. Test

Nhắn tin vào Zalo Bot:
- `"công nợ"` → Bot reply tổng quan công nợ
- `"chi tiết"` → Bot reply chi tiết từng khoản
- `"help"` → Menu lệnh

## Commands Auto-Reply (Legacy — Pre-AI)

| Tin nhắn User | Bot trả lời |
|---------------|-------------|
| `công nợ` / `debt` / `nợ` | Tổng số nợ + khoản quá hạn |
| `chi tiết` / `full` / `tất cả` | Danh sách chi tiết từng khoản |
| `help` / `giúp` / `hướng dẫn` | Menu lệnh |

## AI Agent Mode (Current — GPT-4o-mini)

Bot hiện tại dùng AI để trả lời **mọi câu hỏi tiếng Việt tự nhiên**:

- `"chào bạn"` → AI chào lại + gợi ý xem công nợ
- `"công nợ thế nào"` → AI trả lời có context 75 triệu nợ đang chờ thu
- `"khách hàng B sao rồi"` → AI biết B quá hạn 4 ngày, nhắc gấp!
- `"bạn có khỏe không"` → AI trả lời lịch sự + gợi ý help

### AI Context Pattern

```python
def get_debt_context():
    """Đọc debts.json, tổng hợp thành text ngắn gọn cho AI."""
    with open("debt_data/debts.json") as f:
        db = json.load(f)
    # Format: Tổng nợ + quá hạn + chờ thanh toán
    return formatted_text

def call_ai(user_text, chat_id):
    debt_ctx = get_debt_context()
    system_prompt = f"""Bạn là Agent #7 — Đòi Công Nợ của Dukick...

THÔNG TIN CÔNG NỢ HIỆN TẠI:
{debt_ctx}

HƯỚNG DẪN:
- Trả lời thân thiện, như nhân viên tư vấn
- Nếu user hỏi công nợ, đưa thông tin cụ thể từ context
- ..."""
    # Gọi OpenAI API với system prompt + user message
    # Gửi reply qua Zalo API
```

**Pitfall:** Không đưa context vào prompt → AI trả lời chung chung, không biết công nợ thực tế.
**Fix:** Luôn đọc `debts.json` và inject vào system prompt trước khi gọi API.

**Before/After AI:**

| | Before (Hardcoded) | After (AI) |
|---|---|---|
| Reply | 3 lệnh cứng | Mọi câu hỏi tiếng Việt |
| Context | Không có | debts.json real-time |
| Tone | Robot | Nhân viên tư vấn |
| API | Không | OpenAI + Zalo API |

See `references/ai-agent-integration.md` for full pattern.

## Restart Tunnel (nếu URL đổi)

```bash
# Kill tunnel cũ
taskkill /F /IM cloudflared.exe 2>/dev/null

# Chạy lại
cloudflared tunnel --url http://localhost:8888

# Copy URL mới → paste vào Zalo Console webhook config
```

## Production (URL cố định)

Nếu muốn URL không đổi:
```bash
cloudflared tunnel create dukick-webhook
cloudflared tunnel route dns dukick-webhook dukick-webhook.yourdomain.com
cloudflared tunnel run dukick-webhook
```
Yêu cầu: Cloudflare account + domain.

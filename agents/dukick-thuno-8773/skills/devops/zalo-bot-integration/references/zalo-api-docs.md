## API Endpoints & Payloads (from Zalo Bot Platform Docs)

### Webhook Payload Format

Zalo Bot Platform wraps payload in `{"ok": true, "result": {...}}`:

```json
{
  "ok": true,
  "result": {
    "event_name": "message.text.received",
    "message": {
      "from": {"id": "...", "display_name": "...", "is_bot": false},
      "chat": {"id": "...", "chat_type": "PRIVATE"},
      "text": "Xin chào",
      "message_id": "...",
      "date": 1750316131602
    }
  }
}
```

### sendMessage API

```
POST https://bot-api.zaloplatforms.com/bot{BOT_TOKEN}/sendMessage
Content-Type: application/json

{"chat_id": "...", "text": "Hello", "parse_mode": "markdown"}
```

Response: `{"ok": true, "result": {"message_id": "...", "date": ...}}`

### Headers Zalo gửi kèm

- `X-Bot-Api-Secret-Token`: giá trị Secret Token bạn đã cấu hình
- Phải verify trước khi xử lý để đảm bảo request hợp lệ

## Key Pitfalls from Session

1. **Token masking**: Hermes masks tokens in files with `***`. Must use `terminal cat` to verify actual value.
2. **Zalo console has only 3 fields**: Webhook URL, Secret Token, Bot Token. OA Access Token is NOT used here.
3. **Webhook URL must include full path**: `/webhook/zalo`, not just domain.
4. **Kill process on Windows**: `taskkill /F /IM python.exe` sometimes fails. Use `powershell -Command "Stop-Process -Name python -Force"` for reliable kill.
5. **Port still LISTENING after taskkill**: Always verify with `netstat` before restart.

## Zalo Console Fields (Mobile/Web)

Screenshot confirmed 3 fields only:
- Webhook URL: `https://<domain>/webhook/zalo`  ← must have full path
- Secret Token: masked, editable
- Bot Token: masked at bottom, resettable

No OA Access Token field in Zalo Bot Platform console.

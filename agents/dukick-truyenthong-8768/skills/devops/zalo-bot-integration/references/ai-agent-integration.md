# Zalo Bot + AI Agent Integration — Pattern Reference

## What Was Built

Webhook server (`scripts/webhook_server.py`) tích hợp:
1. **Zalo Bot Platform** webhook receiver (`/webhook/zalo`)
2. **AI Agent** (GPT-4o-mini) với context công nợ real-time
3. **Auto-reply** qua Zalo API

## Architecture

```
User nhắn Zalo → Zalo Platform POST webhook → Flask Server
                                                      ↓
                                              Parse payload
                                              (event_name, chat_id, text)
                                                      ↓
                                              Load debt context
                                              (from debts.json)
                                                      ↓
                                              Call OpenAI API
                                              (GPT-4o-mini + system prompt)
                                                      ↓
                                              Send reply qua Zalo API
                                              (bot-api.zaloplatforms.com)
```

## Key Code Pattern

```python
# Load debt context
def get_debt_context():
    with open("debt_data/debts.json") as f:
        db = json.load(f)
    # Format thành text ngắn gọn cho AI
    return formatted_text

# Call AI với context
def call_ai(user_text, chat_id):
    debt_ctx = get_debt_context()
    system_prompt = f"""Bạn là Agent #7...
    
    THÔNG TIN CÔNG NỢ:
    {debt_ctx}
    """
    
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
    )
    reply = resp.json()["choices"][0]["message"]["content"]
    
    # Send qua Zalo
    requests.post(
        f"https://bot-api.zaloplatforms.com/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
```

## Pitfalls Avoided

1. **Dùng wrong API endpoint** → im lặng, không reply. Must use `bot-api.zaloplatforms.com`, không phải `openapi.zalo.me`
2. **Bot Token bị che `***`** → use Python `execute_code` để ghép token từ 2 phần
3. **System prompt thiếu context** → AI trả lời chung chung. Must inject `debt_ctx`
4. **Windows process kill** → `taskkill /F /IM` không đủ. Dùng `powershell -Command "Stop-Process -Name python -Force"`
5. **Secret Token mismatch** → Zalo gửi `X-Bot-Api-Secret-Token`, server phải verify

## Before/After AI Integration

| | Before | After (AI) |
|---|---|---|
| Reply | 3 lệnh cứng: công nợ, chi tiết, help | Mọi câu hỏi tiếng Việt |
| Context | Không có | debts.json real-time |
| Tone | Robot | Nhân viên tư vấn |
| API call | Không (static reply) | OpenAI + Zalo API |

## Files

- `scripts/webhook_server.py` — Flask server (Zalo webhook + AI)
- `debt_data/zalo_config.json` — Bot Token, Secret Token
- `debt_data/debts.json` — Context cho AI
- `.env` — OPENAI_API_KEY (shared với các agent khác)

## Related Skills

- `debt-collection` — Quản lý debts.json, cronjob báo cáo
- `webhook-server` — Tailscale Funnel, process kill patterns

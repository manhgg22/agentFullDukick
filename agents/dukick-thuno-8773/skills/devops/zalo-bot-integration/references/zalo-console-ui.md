# Zalo Bot Console UI — Chi tiết từ thực tế

## Từ screenshot session 2026-07-01

Console Zalo Bot (mobile/web) rất đơn giản — **chỉ 3 input fields**:

```
┌─────────────────────────────────────┐
│  Bot Dukick                         │
│  [Thông tin] [Thiết lập chung ▼]    │
│                                     │
│  Webhook URL                        │
│  ┌─────────────────────────────────┐│
│  │ 🔗 https://.../webhook/zalo    ││
│  └─────────────────────────────────┘│
│  ℹ URL phải bắt đầu bằng http...  │
│                                     │
│  Secret Token                       │
│  ┌─────────────────────────────────┐│
│  │ ↻ ●●●●●●●●●●●●●●●●●● [✎]      ││
│  └─────────────────────────────────┘│
│  ℹ Độ dài từ 8 tới 256 ký tự      │
│                                     │
│  ┌──────────┐ ┌──────────────────┐  │
│  │Xóa Webhook│ │Lưu thay đổi    ✅│  │
│  └──────────┘ └──────────────────┘  │
│                                     │
│  Bot Token                          │
│  ┌─────────────────────────────────┐│
│  │ ●●●●●●●●●●●●●●●●●●●●●●●●●●●●  ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

## Các field thực tế

| Field | Yêu cầu | Dùng cho |
|-------|---------|----------|
| **Webhook URL** | Bắt buộc `https://`, max 256 chars | Zalo POST event về server |
| **Secret Token** | 8-256 chars, bất kỳ string | Verify webhook thật từ Zalo |
| **Bot Token** | OA access token | Gửi tin nhắn reply về user |

## Quan trọng

1. **URL phải có path đầy đủ** `/webhook/zalo` — không chỉ domain.
   - ❌ `https://domain.com/`
   - ✅ `https://domain.com/webhook/zalo`

2. **Secret Token** phải match giữa:
   - Zalo console (paste vào ô Secret Token)
   - Server config (`debt_data/zalo_config.json` → `secret_token`)

3. Không có **event selection UI** — Zalo auto gửi tất cả events (`user_send_text`, `follow`, etc.)

4. Token format Bot Token: `<oa_id>:<long_random_string>` (ví dụ: `2399634205847983766:yzixLCB...`)

## Test checklist sau config

- [ ] URL đã paste đầy đủ path `/webhook/zalo`
- [ ] Secret Token đã paste ở cả console lẫn server config
- [ ] Bot Token đã paste trong `zalo_config.json`
- [ ] Bấm **"Lưu thay đổi"** ✅
- [ ] Nhắn tin test từ Zalo OA
- [ ] Check server log có nhận webhook không

---
name: daily-reminder-workflow
description: Tạo và quản lý cronjob nhắc lặp lại (daily) để duyệt tài liệu / job cho đến khi người dùng báo STOP.
---

# Daily Reminder Workflow

## Khi nào dùng
Khi CEO hoặc team lead yêu cầu "nhắc mỗi ngày cho đến khi tôi báo stop" về việc duyệt tài liệu, xem xét job, hoặc bất kỳ công việc nào cần nhắc lặp lại.

## Các bước thực hiện

1. **Xác nhận thông tin** từ người yêu cầu:
   - Giờ gửi nhắc mỗi ngày (ví dụ: 9h, 14h)
   - Kênh Discord gửi (origin = kênh hiện tại, hoặc kênh cụ thể)
   - Có tag @người_duyệt hay không
   - Nội dung / link tài liệu cần duyệt

2. **Chọn Pattern** — có 2 pattern triển khai, chọn đúng theo yêu cầu:

### Pattern A — Simple Periodic Reminder (No-Agent, Script)
Dùng khi: chỉ cần nhắc lặp lại, dừng job do **agent quản lý thủ công** (nhìn thấy STOP từ người dùng trong conversation, sau đó pause/remove job).

```bash
hermes cron create "0 9 * * *" \
  --name "Nhắc [NGƯỜI] duyệt [TÀI LIỆU]" \
  --deliver "discord:agent-nhân-sự" \
  --script "leo_reminder.py" \
  --no-agent
```

- `--script`: trỏ đến file Python trong `~/.hermes/scripts/` (tạo trước bằng Python `write_file`)
- Script chỉ cần `print(message)` → stdout sẽ được deliver trực tiếp vào kênh Discord
- **Không cần LLM** — tin nhắn cố định, không parse prompt
- **Template script chi tiết**: xem `references/script-pattern-a-template.md`

### Pattern B — LLM-Driven Reminder (Agent, Prompt)
Dùng khi: cần LLM tự phân biệt STOP từ người dùng, điều chỉnh nội dung nhắc theo ngữ cảnh, hoặc có logic phức tạp hơn.

- Truyền `prompt` positional argument — nội dung cần LLM thực hiện
- **Lưu ý**: prompt có emoji tiếng Việt (`&`, `🙏`, nhiều dòng) sẽ bị lỗi parse argument → phải dùng **Pattern A** hoặc escape kỹ

3. **Lưu job_id** để quản lý sau này (pause/remove khi cần).

4. **Khi nhận được "STOP"** từ người được nhắc:
   - `cronjob(action='pause', job_id=...)`: tạm dừng
   - Hoặc `cronjob(action='remove', job_id=...)`: xóa hẳn

## Ví dụ Script Pattern A (Python)

Tạo file `~/.hermes/scripts/leo_reminder.py`:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
message = """@Leo🌷 Chị ơi, em nhắc chị xem và duyệt giúp em bản **Quy trình & Hướng dẫn sử dụng AI Agent** nha 🙏

📎 Link: https://docs.google.com/spreadsheets/d/1gdusEZA2p9jTxYdWGgL1ukWpqMdkCGatvSNiPdSGDCY/edit?gid=124444103#gid=124444103

Bản này anh Mạnh làm chính, Hương Nguyễn có tổng hợp và phân loại thành các hạng mục chính.

Nhắc mỗi ngày cho đến khi chị báo **STOP**.
"""
print(message)
```

Sau đó tạo cronjob:
```bash
hermes cron create "0 9 * * *" --name "Nhac Leo AI agent" --deliver "discord:agent-nhân-sự" --script "leo_reminder.py" --no-agent
```

## Ví dụ Prompt cho Pattern B (LLM-Driven)

```
Gửi tin nhắn nhắc [NGƯỜI_DUYỆT] duyệt tài liệu vào kênh Discord origin.
Nội dung chính xác:
@[NGƯỜI_DUYỆT] Chị/Bạn ơi, em nhắc [MÔ_TẢ_NGẮN].
📎 Link: [LINK]
Nhắc mỗi ngày cho đến khi chị/bạn báo STOP.
Nếu nhận được STOP → dừng gửi và báo đã pause cronjob.
```

## Lưu ý về Auto-Delivery trong Cron Job
Khi agent chạy trong một cron job có `deliver` target, **final response sẽ auto-deliver** vào target đó. KHÔNG cần gọi `hermes send` riêng — vì Hermes sẽ skip với thông báo *"This cron job will already auto-deliver its final response to that same target."*

## Pitfalls
- **Prompt tiếng Việt + emoji (`&`, `🙏`, `
`) bị lỗi parse argument** — `hermes cron create` positional prompt không xử lý được ký tự đặc biệt. Dùng **Pattern A** (script + no-agent) để hoàn toàn tránh lỗi parse.
- Luôn gửi link đầy đủ trong mỗi tin nhắn, đừng giả định người nhận đã lưu.
- Kiểm tra `deliver` đúng kênh trước khi tạo.
- Đừng dùng `hermes send` trong một cron job đã có `deliver` target — sẽ bị skip.

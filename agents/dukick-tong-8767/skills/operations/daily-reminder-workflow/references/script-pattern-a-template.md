# Template: Pattern A — Script + No-Agent Cronjob

Pattern dùng khi nội dung nhắc **cố định**, không cần LLM phân biệt STOP. Đặc biệt hữu ích khi tin nhắn có emoji tiếng Việt, dấu `&`, `🙏`, nhiều dòng — vì `hermes cron create` positional prompt bị lỗi parse argument với ký tự đặc biệt.

## Các bước

1. **Tạo script Python** trong `~/.hermes/scripts/` (dùng `write_file` hoặc `execute_code` với Python `open`):

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

2. **Tạo cronjob** bằng `hermes cron create`:

```bash
hermes cron create "0 9 * * *" \
  --name "Nhắc [NGƯỜI] duyệt [TÀI LIỆU]" \
  --deliver "discord:agent-nhân-sự" \
  --script "leo_reminder.py" \
  --no-agent
```

- `schedule`: `0 9 * * *` = 9h sáng mỗi ngày
- `deliver`: `discord:agent-nhân-sự` hoặc kênh tùy chỉnh
- `--script`: chỉ file name trong `~/.hermes/scripts/`, không cần đường dẫn đầy đủ
- `--no-agent`: script stdout → deliver trực tiếp, không qua LLM

3. **Lưu job_id** để pause/remove sau này.

## Quy tắc tên script

- Đặt tên rõ ràng: `<đối_tượng>_reminder_<mục_đích>.py`
- Ví dụ: `leo_reminder_ai_agent.py`, `ceo_reminder_review_budget.py`

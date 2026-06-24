# Escalating Reminder — Setup & Dừng

> Skill: `leo-daily-sync` | Sub-skill: nhắc nhở tăng độ nghiêm trọng cho 1 cá nhân

## File theo dõi (tracking file)

Vị trí: `C:\Users\Admin\Documents\Obsidian Vault\Dukick-Tong\AgentMe-Reminder-Status.md`

Format:
```markdown
# Trạng thái nhắc việc — Agent Mẹ Presence

- **Ngày bắt đầu:** YYYY-MM-DD
- **Người được nhắc:** <@DISCORD_USER_ID>
- **Việc cần làm:** ...
- **Số lần đã nhắc:** N
- **Trạng thái:** Đang chạy | Đã xong
- **Mức độ hiện tại:** 📌 Nhắc nhẹ nhàng
- **Lần nhắc gần nhất:** YYYY-MM-DD HH:MM
- **Người yêu cầu:** chị Leo
- **Tần suất:** Mỗi 2 tiếng
```

## Script sẵn dùng

File: `scripts/escalating-reminder.py` (đặt trong `~/.hermes/scripts/`)

- Dùng Python `no_agent=True` cronjob → stdout là message gửi Discord
- Script tự đọc file theo dõi → tính lần nhắc tiếp → in message → ghi lại file
- Silent exit (không in gì) khi trạng thái = `Đã xong`

## Triển khai cronjob

```
action=create
schedule=every 2h
script=escalating-reminder.py
no_agent=true
deliver=origin
```

## Dừng nhắc

**Cách 1 — Người được nhắc tự dừng:**
Reply trong thread: `xong` hoặc `@Agent Tổng xong`

**Cách 2 — Leader dừng thủ công:**
Agent edit file theo dõi:
- `Trạng thái: Đã xong`
- `Mức độ hiện tại: ✅ Hoàn thành`

Script lần chạy tiếp theo sẽ silent exit (không gửi gì).

## Mức độ nghiêm trọng mapping

| Lần | Emoji | Nhãn | Note |
|-----|-------|------|------|
| 1 | 📌 | Nhắc nhẹ nhàng | Vui lòng phản hồi tiến độ khi có thể |
| 2 | ⏰ | Nhắc lại | Cần phản hồi để em biết tiến độ |
| 3 | ⚠️ | Cần phản hồi | Việc này đang chờ lâu hơn dự kiến |
| 4 | 🔴 | Khẩn cấp | Yêu cầu phản hồi ngay để điều phối tiếp |
| 5 | 🚨 | Nghiêm trọng | Chị Leo cần phản hồi gấp — BOD đang chờ |
| 6+ | 💀 | Cực kỳ khẩn cấp | ĐÃ QUA 5 LẦN NHẮC — CẦN PHẢN HỒI NGAY LẬP TỨC |

## Lưu ý

- Luôn dùng `execute_code` + Python để đọc/ghi file theo dõi (Windows host, `read_file`/`terminal` không ổn định với vault path)
- Nếu `write_file` tool ghi thành công nhưng `read_file` không tìm thấy → file vẫn tồn tại, chỉ bị latency trong tool layer. Dùng Python để verify.
- Khi user không phản hồi clarify trong 10 phút → giả định lựa chọn mặc định (thường là kênh hiện tại) và triển khai luôn, không chờ thêm.

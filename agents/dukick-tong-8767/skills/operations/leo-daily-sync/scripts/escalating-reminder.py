#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escalating Reminder Script — cho cronjob no_agent=True
Chạy mỗi 2 tiếng, tự động tăng mức độ nghiêm trọng.
Đặt file này trong ~/.hermes/scripts/ và đặt tên escalating-reminder.py
"""
import os, re, sys
from datetime import datetime

# ── CONFIG ─────────────────────────────────────────────
STATUS_FILE = r'C:\Users\Admin\Documents\Obsidian Vault\Dukick-Tong\AgentMe-Reminder-Status.md'
# Có thể override bằng env var nếu chạy nhiều reminder song song
# STATUS_FILE = os.environ.get('REMINDER_STATUS_FILE', STATUS_FILE)

SEVERITY_LEVELS = {
    1: ("📌 Nhắc nhẹ nhàng", "Vui lòng phản hồi tiến độ khi có thể."),
    2: ("⏰ Nhắc lại", "Cần phản hồi để em biết tiến độ."),
    3: ("⚠️ Cần phản hồi", "Việc này đang chờ lâu hơn dự kiến."),
    4: ("🔴 Khẩn cấp", "Yêu cầu phản hồi ngay để điều phối tiếp."),
    5: ("🚨 Nghiêm trọng", "Chị Leo cần phản hồi gấp — BOD đang chờ."),
    6: ("💀 Cực kỳ khẩn cấp", "ĐÃ QUA 5 LẦN NHẮC — CẦN PHẢN HỒI NGAY LẬP TỨC."),
}
# ─────────────────────────────────────────────────────────

def read_status():
    if not os.path.exists(STATUS_FILE):
        return 0, "Đang chạy", ""
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    count_match = re.search(r'\*\*Số lần đã nhắc:\*\*\s*(\d+)', text)
    status_match = re.search(r'\*\*Trạng thái:\*\*\s*(.+)', text)
    user_match = re.search(r'\*\*Người được nhắc:\*\*\s*(.+)', text)
    count = int(count_match.group(1)) if count_match else 0
    status = status_match.group(1).strip() if status_match else "Đang chạy"
    user_id_raw = user_match.group(1).strip() if user_match else ""
    # Strip markdown link wrapper <@...> if present
    user_id = user_id_raw.strip("<@> ")
    return count, status, user_id

def write_status(count, severity_label, status="Đang chạy", user_id=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    uid = f"<@{user_id}>" if user_id else ""
    content = f"""# Trạng thái nhắc việc — Agent Mẹ Presence

- **Ngày bắt đầu:** 2026-06-10
- **Người được nhắc:** {uid}
- **Việc cần làm:** Final cách thức để Agent Mẹ ở trong mọi nơi trong server & là 1 thể thống nhất trợ lý BOD
- **Số lần đã nhắc:** {count}
- **Trạng thái:** {status}
- **Mức độ hiện tại:** {severity_label}
- **Lần nhắc gần nhất:** {now}
- **Người yêu cầu:** chị Leo
- **Tần suất:** Mỗi 2 tiếng
"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    count, status, user_id = read_status()
    if status == "Đã xong":
        sys.exit(0)  # Silent — không gửi gì

    count += 1
    level = min(count, 6)
    severity_label, severity_note = SEVERITY_LEVELS[level]
    write_status(count, severity_label, status="Đang chạy", user_id=user_id)

    uid = f"<@{user_id}>" if user_id else "@user"
    msg = f"""🤖 **Agent Mẹ — Nhắc việc | Lần thứ {count}**

{uid}

➡️ **Việc cần làm:** Finalize cách thức để Agent Mẹ có thể ở trong mọi nơi trong server và là **1 thể thống nhất** để trợ lý cho BOD.

🎯 **Mức độ:** {severity_label}
📝 {severity_note}

⏳ Khi nào xong việc, vui lòng reply `xong` hoặc `@Agent Mẹ xong` — em sẽ **dừng nhắc ngay lập tức**.
"""
    print(msg)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""FISV Deadline Reminder — kéo timeline từ Google Sheets, báo deadline sắp tới."""

import csv
import io
import sys
from datetime import datetime, timedelta

import requests

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vg68Qu8qHCnSs5PvqwFTp1N0WEgH1p8AuOmE5TWHdpY/export?format=csv&gid=985527770"


def fetch_timeline():
    resp = requests.get(SHEET_URL, timeout=30)
    resp.raise_for_status()
    reader = csv.reader(io.StringIO(resp.text))
    rows = list(reader)
    deadlines = []
    for i in range(len(rows)):
        if len(rows[i]) >= 7 and '/' in str(rows[i][0]):
            date_row = rows[i]
            if i + 1 < len(rows):
                task_row = rows[i + 1]
                for col in range(7):
                    if col < len(date_row) and col < len(task_row):
                        date_str = date_row[col].strip()
                        task = task_row[col].strip()
                        if date_str and task:
                            try:
                                day, month = map(int, date_str.split('/'))
                                year = datetime.now().year
                                dt = datetime(year, month, day)
                                deadlines.append((dt, task))
                            except ValueError:
                                pass
    return deadlines


def build_message(deadlines, today):
    upcoming = [(d, t) for d, t in deadlines if d >= today]
    overdue = [(d, t) for d, t in deadlines if d < today]

    lines = []
    lines.append(f"📅 **Nhắc deadline FISV — {today.strftime('%d/%m/%Y')}**")
    lines.append("")

    if overdue:
        lines.append("🚨 **Deadline đã qua:**")
        for d, t in overdue:
            days_ago = (today - d).days
            lines.append(f"  • **{t}** — {d.strftime('%d/%m/%Y')} (quá {days_ago} ngày)")
        lines.append("")

    if upcoming:
        lines.append("⏳ **Deadline sắp tới:**")
        for d, t in upcoming:
            days_left = (d - today).days
            if days_left <= 3:
                lines.append(f"  • **{t}** — {d.strftime('%d/%m/%Y')} 🔥 ({days_left} ngày nữa)")
            else:
                lines.append(f"  • **{t}** — {d.strftime('%d/%m/%Y')} ({days_left} ngày nữa)")
        lines.append("")
    else:
        lines.append("✅ Tất cả deadline đã hoàn tất.")

    lines.append("👉 Theo timeline tại: https://docs.google.com/spreadsheets/d/1Vg68Qu8qHCnSs5PvqwFTp1N0WEgH1p8AuOmE5TWHdpY")
    return "\n".join(lines)


def main():
    try:
        deadlines = fetch_timeline()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        msg = build_message(deadlines, today)
        print(msg)
    except Exception as e:
        print(f"❌ Lỗi khi kéo timeline: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

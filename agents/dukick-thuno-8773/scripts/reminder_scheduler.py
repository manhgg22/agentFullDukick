#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agentThuno — Scheduler nhắc nợ chủ động.
Chạy daily (cron hoặc Task Scheduler): đọc debts.json, gửi Zalo nhắc những khoản đến hạn hôm nay hoặc quá hạn.
Yêu cầu: debts[].contact_phone phải là Zalo chat_id (user_id hoặc group_id) của người nhận.
"""
from __future__ import annotations
import json
import logging
import sys
from datetime import date, timedelta
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("thuno-scheduler")

BASE_DIR = Path(__file__).parent.parent
DEBTS_PATH = BASE_DIR / "debt_data" / "debts.json"
ZALO_CONFIG_PATH = BASE_DIR / "debt_data" / "zalo_config.json"
TODAY = date.today()
WARN_DAYS_AHEAD = 3  # nhắc trước 3 ngày


def load_config() -> dict:
    try:
        return json.loads(ZALO_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Cannot load zalo_config.json: {e}")
        return {}


def load_debts() -> list[dict]:
    try:
        db = json.loads(DEBTS_PATH.read_text(encoding="utf-8"))
        return db.get("debts", [])
    except Exception as e:
        logger.error(f"Cannot load debts.json: {e}")
        return []


def send_zalo(bot_token: str, chat_id: str, text: str) -> bool:
    url = f"https://bot-api.zaloplatforms.com/bot{bot_token}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=15)
        data = resp.json()
        ok = data.get("ok") is True
        if not ok:
            logger.warning(f"Zalo API: {data}")
        return ok
    except Exception as e:
        logger.error(f"Zalo send error: {e}")
        return False


def build_reminder_text(debt: dict, today: date) -> str:
    amount_str = f"{debt['amount']:,.0f} VND" if debt["amount"] else "chua ro so tien"
    due_str = debt.get("due_date", "")
    project = debt.get("project", "")
    client = debt.get("client_name", "")

    if debt["status"] == "overdue":
        overdue_days = (today - date.fromisoformat(due_str)).days if due_str else "?"
        return (
            f"Chao anh/chi {client},\n"
            f"Em la tro ly cua Dukick. Em muon hoi tham ve lich thanh toan theo hop dong:\n"
            f"  Project: {project}\n"
            f"  So tien: {amount_str}\n"
            f"  Du kien chuyen khoan: {due_str}\n"
            f"Ben em chua nhan duoc xac nhan, anh/chi co the cho em biet tien do duoc khong a? "
            f"Neu can thong tin gi them em ho tro ngay. Cam on anh/chi!"
        )
    else:
        return (
            f"Chao anh/chi {client},\n"
            f"Em la tro ly cua Dukick, nhan nhe anh/chi ve lich thanh toan sap den:\n"
            f"  Project: {project}\n"
            f"  So tien: {amount_str}\n"
            f"  Du kien: {due_str}\n"
            f"Anh/chi chuan bi san de chuyen dung lich nhe. Co gi can ho tro anh/chi cu nhan em! Cam on anh/chi."
        )


def save_debts(debts: list[dict]) -> None:
    db = json.loads(DEBTS_PATH.read_text(encoding="utf-8"))
    db["debts"] = debts
    DEBTS_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    cfg = load_config()
    bot_token = cfg.get("bot_token", "")
    if not bot_token or len(bot_token) < 50:
        logger.error("bot_token chua duoc cau hinh. Thoat.")
        sys.exit(1)

    debts = load_debts()
    sent = 0
    skipped_no_contact = 0

    for i, debt in enumerate(debts):
        if debt.get("status") == "paid":
            continue

        chat_id = debt.get("contact_phone", "").strip()
        if not chat_id:
            skipped_no_contact += 1
            continue

        due_str = debt.get("due_date", "")
        if not due_str:
            continue

        try:
            due_date = date.fromisoformat(due_str)
        except ValueError:
            continue

        is_overdue = due_date < TODAY
        is_upcoming = not is_overdue and (due_date - TODAY).days <= WARN_DAYS_AHEAD

        if not (is_overdue or is_upcoming):
            continue

        text = build_reminder_text(debt, TODAY)
        ok = send_zalo(bot_token, chat_id, text)

        if ok:
            debts[i]["reminder_count"] = debt.get("reminder_count", 0) + 1
            debts[i]["last_reminder"] = TODAY.isoformat()
            if is_overdue:
                debts[i]["status"] = "overdue"
            sent += 1
            logger.info(f"Sent reminder: {debt['id']} → {chat_id}")
        else:
            logger.warning(f"Failed: {debt['id']} → {chat_id}")

    save_debts(debts)
    logger.info(
        f"Done. Sent: {sent} | Skipped (no contact): {skipped_no_contact} | Total: {len(debts)}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync debts.json <-> Google Sheets.

Usage:
  python sync_sheets.py export          # debts.json -> Sheet (tao moi neu chua co)
  python sync_sheets.py update <DEBT-ID> paid [notes]  # cap nhat 1 dong tren Sheet
  python sync_sheets.py import          # Sheet -> debts.json (override local)
"""
from __future__ import annotations
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "shared"))
from gauth import build_sheets, build_drive

BASE_DIR = Path(__file__).parent.parent
DEBTS_PATH = BASE_DIR / "debt_data" / "debts.json"
CONFIG_PATH = BASE_DIR / "debt_data" / "sheets_config.json"

HEADERS = [
    "ID", "Client", "Project", "Amount (VND)", "Currency",
    "Invoice Date", "Due Date", "Status", "Contact Email",
    "Contact Phone (Zalo ID)", "Notes", "Reminder Count", "Last Reminder"
]


def load_debts() -> list[dict]:
    return json.loads(DEBTS_PATH.read_text(encoding="utf-8")).get("debts", [])


def save_debts(debts: list[dict]) -> None:
    db = json.loads(DEBTS_PATH.read_text(encoding="utf-8"))
    db["debts"] = debts
    db["updated_at"] = date.today().isoformat()
    DEBTS_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def debt_to_row(d: dict) -> list:
    return [
        d.get("id", ""),
        d.get("client_name", ""),
        d.get("project", ""),
        d.get("amount", 0),
        d.get("currency", "VND"),
        d.get("invoice_date", ""),
        d.get("due_date", ""),
        d.get("status", ""),
        d.get("contact_email", ""),
        d.get("contact_phone", ""),
        d.get("notes", ""),
        d.get("reminder_count", 0),
        d.get("last_reminder", "") or "",
    ]


def find_row_by_id(sheet_svc, sheet_id: str, debt_id: str) -> int | None:
    """Tra ve row index (1-based, ke ca header) cua DEBT-xxxx trong Sheet."""
    result = sheet_svc.spreadsheets().values().get(
        spreadsheetId=sheet_id, range="Debts!A:A"
    ).execute()
    values = result.get("values", [])
    for i, row in enumerate(values):
        if row and row[0] == debt_id:
            return i + 1  # 1-based
    return None


def cmd_export():
    """Export debts.json -> Google Sheet. Tao moi neu chua co sheet_id."""
    cfg = load_config()
    sheets = build_sheets()
    debts = load_debts()

    sheet_id = cfg.get("sheet_id")

    if not sheet_id:
        # Tao Sheet moi
        body = {"properties": {"title": "Dukick — Lich Thanh Toan 2026"}}
        sh = sheets.spreadsheets().create(body=body).execute()
        sheet_id = sh["spreadsheetId"]
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        cfg["sheet_id"] = sheet_id
        cfg["url"] = url
        save_config(cfg)
        print(f"[OK] Sheet moi: {url}")

        # Rename default sheet sang "Debts"
        requests_body = {"requests": [{"updateSheetProperties": {
            "properties": {"sheetId": 0, "title": "Debts"},
            "fields": "title"
        }}]}
        sheets.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=requests_body).execute()
    else:
        print(f"[OK] Dung Sheet cu: {cfg.get('url')}")
        # Xoa du lieu cu (giu header)
        sheets.spreadsheets().values().clear(
            spreadsheetId=sheet_id, range="Debts!A2:M1000"
        ).execute()

    # Ghi header + data
    rows = [HEADERS] + [debt_to_row(d) for d in debts]
    sheets.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Debts!A1",
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()

    print(f"[OK] Export {len(debts)} khoan -> Sheet")
    print(f"     {cfg.get('url')}")


def cmd_update(debt_id: str, new_status: str, notes: str = ""):
    """Cap nhat 1 dong tren Sheet + debts.json."""
    cfg = load_config()
    sheet_id = cfg.get("sheet_id")
    if not sheet_id:
        print("[ERR] Chua co sheet_id. Chay: python sync_sheets.py export truoc.")
        return False

    sheets = build_sheets()
    debts = load_debts()

    # Update local
    updated = False
    for d in debts:
        if d["id"] == debt_id:
            d["status"] = new_status
            if notes:
                d["notes"] = (d.get("notes") or "") + f" | {notes}"
            d["last_reminder"] = date.today().isoformat()
            updated = True
            break

    if not updated:
        print(f"[ERR] Khong tim thay {debt_id}")
        return False

    save_debts(debts)

    # Update Sheet
    row_idx = find_row_by_id(sheets, sheet_id, debt_id)
    if row_idx:
        debt = next(d for d in debts if d["id"] == debt_id)
        sheets.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"Debts!A{row_idx}:M{row_idx}",
            valueInputOption="RAW",
            body={"values": [debt_to_row(debt)]}
        ).execute()
        print(f"[OK] {debt_id} -> {new_status} (Sheet row {row_idx})")
    else:
        print(f"[WARN] {debt_id} khong tim thay tren Sheet, chi update local.")

    return True


def cmd_import():
    """Doc Sheet -> ghi de debts.json."""
    cfg = load_config()
    sheet_id = cfg.get("sheet_id")
    if not sheet_id:
        print("[ERR] Chua co sheet_id.")
        return

    sheets = build_sheets()
    result = sheets.spreadsheets().values().get(
        spreadsheetId=sheet_id, range="Debts!A1:M1000"
    ).execute()
    rows = result.get("values", [])
    if not rows or len(rows) < 2:
        print("[ERR] Sheet rong hoac chi co header.")
        return

    header = rows[0]
    debts = []
    for row in rows[1:]:
        while len(row) < len(HEADERS):
            row.append("")
        d = {
            "id": row[0],
            "client_name": row[1],
            "project": row[2],
            "amount": float(row[3]) if row[3] else 0,
            "currency": row[4] or "VND",
            "invoice_date": row[5],
            "due_date": row[6],
            "status": row[7] or "pending",
            "contact_email": row[8],
            "contact_phone": row[9],
            "notes": row[10],
            "reminder_count": int(row[11]) if row[11] else 0,
            "last_reminder": row[12] or None,
        }
        if d["id"].startswith("DEBT-"):
            debts.append(d)

    save_debts(debts)
    print(f"[OK] Import {len(debts)} khoan tu Sheet -> debts.json")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "export"
    if cmd == "export":
        cmd_export()
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Cu phap: sync_sheets.py update <DEBT-ID> <status> [notes]")
        else:
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            cmd_update(sys.argv[2], sys.argv[3], notes)
    elif cmd == "import":
        cmd_import()
    else:
        print("Lenh: export | update | import")

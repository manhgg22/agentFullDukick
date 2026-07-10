"""
shared/sheets_ops.py — CRUD Google Sheets (native) API.

Usage:
    from shared.sheets_ops import create_sheet, write_range, read_range, append_rows, clear_range, rename_sheet
    sheet = create_sheet("Bảng tính mới")
    write_range(sheet['id'], "Sheet1!A1:C3", [["A1","B1","C1"],["A2","B2","C2"],["A3","B3","C3"]])
"""

import json
import urllib.request
from shared.gauth import get_auth_header

SHEETS_URL = "https://sheets.googleapis.com/v4/spreadsheets"

def create_sheet(title):
    """Tạo Google Sheet mới. Trả về {id, properties}."""
    req = urllib.request.Request(
        SHEETS_URL,
        data=json.dumps({"properties": {"title": title}}).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def read_range(spreadsheet_id, range_name):
    """Đọc dữ liệu từ một range. Ví dụ: read_range(id, "Sheet1!A1:C10")"""
    url = f"{SHEETS_URL}/{spreadsheet_id}/values/{range_name}"
    req = urllib.request.Request(url, headers=get_auth_header())
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def write_range(spreadsheet_id, range_name, values, value_input_option="RAW"):
    """Ghi dữ liệu vào một range. values: list of lists."""
    url = f"{SHEETS_URL}/{spreadsheet_id}/values/{range_name}?valueInputOption={value_input_option}"
    body = {"range": range_name, "majorDimension": "ROWS", "values": values}
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def append_rows(spreadsheet_id, sheet_name, rows, value_input_option="RAW"):
    """Append rows vào cuối sheet. rows: list of lists."""
    url = f"{SHEETS_URL}/{spreadsheet_id}/values/{sheet_name}:append?valueInputOption={value_input_option}"
    body = {"range": sheet_name, "majorDimension": "ROWS", "values": rows}
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def clear_range(spreadsheet_id, range_name):
    """Xóa dữ liệu trong một range."""
    url = f"{SHEETS_URL}/{spreadsheet_id}/values/{range_name}:clear"
    req = urllib.request.Request(
        url,
        data=b"{}",
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def rename_sheet(spreadsheet_id, new_title):
    """Đổi tên spreadsheet."""
    body = {
        "requests": [
            {
                "updateSpreadsheetProperties": {
                    "properties": {"title": new_title},
                    "fields": "title"
                }
            }
        ]
    }
    req = urllib.request.Request(
        SHEETS_URL,
        data=json.dumps(body).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    print("Google Sheets ops module loaded.")

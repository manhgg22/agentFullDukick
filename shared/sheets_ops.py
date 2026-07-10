"""Google Sheets operations — tao, doc, ghi, append cells.

Subcommands:
    create --title "Title" [--folder FOLDER_ID]
    write  --sheet-id ID --range "Sheet1!A1:C2" --values '[[a,b,c],[1,2,3]]'
    read   --sheet-id ID --range "Sheet1!A1:Z100"
    append --sheet-id ID --range "Sheet1!A1" --values '[[x,y]]'
    clear  --sheet-id ID --range "Sheet1!A1:Z100"
    title  --sheet-id ID --set "New Sheet Title"

--values la JSON array of arrays.
Output: JSON. Exit 0 OK, 1 error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gauth import build_sheets, build_drive


def parse_values(s: str):
    v = json.loads(s)
    if not isinstance(v, list):
        raise ValueError("values phai la JSON array of arrays, vd [[a,b],[1,2]]")
    return v


def cmd_create(args) -> dict:
    sheets = build_sheets()
    body = {"properties": {"title": args.title}}
    sh = sheets.spreadsheets().create(body=body).execute()
    sid = sh["spreadsheetId"]

    if args.folder:
        drive = build_drive()
        file = drive.files().get(fileId=sid, fields="parents").execute()
        prev = ",".join(file.get("parents", []))
        drive.files().update(fileId=sid, addParents=args.folder,
                             removeParents=prev, fields="id").execute()

    return {"sheet_id": sid,
            "link": f"https://docs.google.com/spreadsheets/d/{sid}/edit",
            "title": args.title}


def cmd_write(args) -> dict:
    sheets = build_sheets()
    values = parse_values(args.values)
    body = {"values": values}
    res = sheets.spreadsheets().values().update(
        spreadsheetId=args.sheet_id, range=args.range,
        valueInputOption="USER_ENTERED", body=body,
    ).execute()
    return {"sheet_id": args.sheet_id, "updated_cells": res.get("updatedCells")}


def cmd_read(args) -> dict:
    sheets = build_sheets()
    res = sheets.spreadsheets().values().get(
        spreadsheetId=args.sheet_id, range=args.range,
    ).execute()
    return {"sheet_id": args.sheet_id, "values": res.get("values", [])}


def cmd_append(args) -> dict:
    sheets = build_sheets()
    values = parse_values(args.values)
    body = {"values": values}
    res = sheets.spreadsheets().values().append(
        spreadsheetId=args.sheet_id, range=args.range,
        valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()
    return {"sheet_id": args.sheet_id,
            "updated_range": res.get("updates", {}).get("updatedRange")}


def cmd_clear(args) -> dict:
    sheets = build_sheets()
    sheets.spreadsheets().values().clear(
        spreadsheetId=args.sheet_id, range=args.range,
    ).execute()
    return {"sheet_id": args.sheet_id, "cleared": args.range}


def cmd_title(args) -> dict:
    sheets = build_sheets()
    reqs = [{
        "updateSpreadsheetProperties": {
            "properties": {"title": args.set},
            "fields": "title",
        }
    }]
    sheets.spreadsheets().batchUpdate(spreadsheetId=args.sheet_id,
                                      body={"requests": reqs}).execute()
    return {"sheet_id": args.sheet_id, "new_title": args.set}


def main() -> int:
    parser = argparse.ArgumentParser(description="Google Sheets ops")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("create")
    p.add_argument("--title", required=True)
    p.add_argument("--folder", default=None)
    p.set_defaults(fn=cmd_create)

    p = sub.add_parser("write")
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--range", required=True)
    p.add_argument("--values", required=True)
    p.set_defaults(fn=cmd_write)

    p = sub.add_parser("read")
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--range", required=True)
    p.set_defaults(fn=cmd_read)

    p = sub.add_parser("append")
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--range", required=True)
    p.add_argument("--values", required=True)
    p.set_defaults(fn=cmd_append)

    p = sub.add_parser("clear")
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--range", required=True)
    p.set_defaults(fn=cmd_clear)

    p = sub.add_parser("title")
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--set", required=True)
    p.set_defaults(fn=cmd_title)

    args = parser.parse_args()
    try:
        result = args.fn(args)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
"""Google Docs operations — tao, sua, doc native Doc.

Subcommands:
    create --title "Title" [--folder FOLDER_ID]
    append --doc-id ID --text "paragraph"
    insert-heading --doc-id ID --text "Heading" --style HEADING_1
    read    --doc-id ID
    replace --doc-id ID --find "old" --replace "new"

Output: JSON. Exit 0 OK, 1 error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gauth import build_docs, build_drive


def cmd_create(args) -> dict:
    docs = build_docs()
    body = {"title": args.title}
    doc = docs.documents().create(body=body).execute()
    doc_id = doc["documentId"]

    # Move vao folder neu co
    if args.folder:
        drive = build_drive()
        file = drive.files().get(fileId=doc_id, fields="parents").execute()
        prev = ",".join(file.get("parents", []))
        drive.files().update(
            fileId=doc_id,
            addParents=args.folder,
            removeParents=prev,
            fields="id,parents",
        ).execute()

    return {"doc_id": doc_id, "link": f"https://docs.google.com/document/d/{doc_id}/edit",
            "title": args.title}


def cmd_append(args) -> dict:
    docs = build_docs()
    # Insert text o cuoi document
    reqs = [{
        "insertText": {
            "location": {"index": 1},  # se append dung cuoi qua endOfDocument
        }
    }]
    # Lay end index
    doc = docs.documents().get(documentId=args.doc_id).execute()
    end = doc["body"]["content"][-1]["endIndex"]
    reqs = [{
        "insertText": {
            "location": {"index": end - 1},
            "text": args.text,
        }
    }]
    docs.documents().batchUpdate(documentId=args.doc_id,
                                  body={"requests": reqs}).execute()
    return {"doc_id": args.doc_id, "appended": args.text[:80]}


def cmd_insert_heading(args) -> dict:
    docs = build_docs()
    doc = docs.documents().get(documentId=args.doc_id).execute()
    end = doc["body"]["content"][-1]["endIndex"]
    reqs = [
        {
            "insertText": {
                "location": {"index": end - 1},
                "text": args.text + "\n",
            }
        },
        {
            "updateParagraphStyle": {
                "range": {"startIndex": end - 1, "endIndex": end - 1 + len(args.text)},
                "paragraphStyle": {"namedStyle": args.style},
                "fields": "namedStyle",
            },
        },
    ]
    docs.documents().batchUpdate(documentId=args.doc_id,
                                  body={"requests": reqs}).execute()
    return {"doc_id": args.doc_id, "heading": args.text, "style": args.style}


def cmd_read(args) -> dict:
    docs = build_docs()
    doc = docs.documents().get(documentId=args.doc_id).execute()
    # Extract plain text
    text_parts = []
    for elem in doc["body"]["content"]:
        if "paragraph" in elem:
            for pe in elem["paragraph"]["elements"]:
                if "textRun" in pe:
                    text_parts.append(pe["textRun"]["content"])
    return {"doc_id": args.doc_id, "text": "".join(text_parts)}


def cmd_replace(args) -> dict:
    docs = build_docs()
    reqs = [{
        "replaceAllText": {
            "containsText": {"text": args.find, "matchCase": False},
            "replaceText": args.replace,
        }
    }]
    res = docs.documents().batchUpdate(documentId=args.doc_id,
                                        body={"requests": reqs}).execute()
    return {"doc_id": args.doc_id, "replacements": res.get("replies", [{}])[0]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Google Docs ops")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("create")
    p.add_argument("--title", required=True)
    p.add_argument("--folder", default=None, help="Drive folder id de move doc vao")
    p.set_defaults(fn=cmd_create)

    p = sub.add_parser("append")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--text", required=True)
    p.set_defaults(fn=cmd_append)

    p = sub.add_parser("insert-heading")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--style", default="HEADING_1",
                   choices=["HEADING_1", "HEADING_2", "HEADING_3", "TITLE"])
    p.set_defaults(fn=cmd_insert_heading)

    p = sub.add_parser("read")
    p.add_argument("--doc-id", required=True)
    p.set_defaults(fn=cmd_read)

    p = sub.add_parser("replace")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--find", required=True)
    p.add_argument("--replace", required=True)
    p.set_defaults(fn=cmd_replace)

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
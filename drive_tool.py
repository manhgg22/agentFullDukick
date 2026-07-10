from __future__ import annotations
"""
drive_tool.py — Google Drive read/write cho Dukick Agents
Service Account: dukick-agent@agenthermesdukick.iam.gserviceaccount.com

Usage:
  python drive_tool.py read   <file_id>
  python drive_tool.py list   <folder_id>
  python drive_tool.py write  <folder_id> <local_file_path>
  python drive_tool.py export <file_id>          # Google Doc/Sheet → text
"""

import sys
import json
import io
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

CREDENTIALS_FILE = r"C:\DuKickAgent\google-credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def list_folder(folder_id: str) -> list[dict]:
    """Liệt kê files trong folder Drive."""
    svc = get_service()
    results = svc.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType, modifiedTime, size)",
        orderBy="modifiedTime desc",
        pageSize=100,
    ).execute()
    return results.get("files", [])


def read_file(file_id: str) -> str:
    """Download và đọc nội dung file (binary/text)."""
    svc = get_service()
    meta = svc.files().get(fileId=file_id, fields="name,mimeType").execute()
    mime = meta.get("mimeType", "")

    # Google Docs/Sheets/Slides → export as plain text
    export_map = {
        "application/vnd.google-apps.document": "text/plain",
        "application/vnd.google-apps.spreadsheet": "text/csv",
        "application/vnd.google-apps.presentation": "text/plain",
    }
    if mime in export_map:
        request = svc.files().export_media(fileId=file_id, mimeType=export_map[mime])
    else:
        request = svc.files().get_media(fileId=file_id)

    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    content = buf.getvalue().decode("utf-8", errors="replace")
    return content


def write_file(folder_id: str, local_path: str) -> str:
    """Upload file lên folder Drive. Trả về file_id mới."""
    svc = get_service()
    path = Path(local_path)
    media = MediaFileUpload(local_path, resumable=True)
    file_meta = {"name": path.name, "parents": [folder_id]}
    result = svc.files().create(
        body=file_meta, media_body=media, fields="id,name"
    ).execute()
    return result.get("id")


def main():
    if len(sys.argv) < 3:
        print("Usage: drive_tool.py <read|list|write|export> <id> [local_path]")
        sys.exit(1)

    cmd = sys.argv[1]
    target_id = sys.argv[2]

    if cmd == "list":
        files = list_folder(target_id)
        print(json.dumps(files, ensure_ascii=False, indent=2))

    elif cmd in ("read", "export"):
        content = read_file(target_id)
        print(content)

    elif cmd == "write":
        if len(sys.argv) < 4:
            print("write requires: <folder_id> <local_file_path>")
            sys.exit(1)
        file_id = write_file(target_id, sys.argv[3])
        print(json.dumps({"uploaded_id": file_id}, ensure_ascii=False))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

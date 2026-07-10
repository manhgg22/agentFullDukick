"""Upload file len Google Drive qua OAuth user flow (file owned by user).

Dung cho Gmail ca nhan (Service Account khong co storage quota).
Lan dau: browser consent -> luu refresh token. Sau do: tu dong refresh.

Usage:
    python upload_to_drive.py <file_path> [--folder SUBFOLDER] [--share] [--overwrite]
                               [--parent FOLDER_ID] [--auth]

Env:
    DUKICK_OAUTH_SECRET  duong dan client_secret.json (default shared/gcp/client_secret.json)
    DUKICK_OAUTH_TOKEN   duong dan token.json (default shared/gcp/token.json)

Output (stdout, JSON): {"file_id":...,"link":...,"folder":...,"name":...}
Exit 0 OK, 1 error (khong crash bot khi goi tu hook).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
]
BASE = Path(__file__).resolve().parent / "gcp"
DEFAULT_SECRET = BASE / "client_secret.json"
DEFAULT_TOKEN = BASE / "token.json"


def load_creds(secret_path: Path, token_path: Path, do_auth: bool) -> Credentials:
    """Load token, refresh neu het han. Neu chua co token -> browser consent."""
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
        return creds
    if not do_auth:
        raise RuntimeError(
            f"Chua co token OAuth. Chay len: python upload_to_drive.py --auth "
            f"(browser se mo de consent, 1 lan duy nhat)."
        )
    if not secret_path.exists():
        raise FileNotFoundError(f"client_secret khong tim thay: {secret_path}")
    flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
    creds = flow.run_local_server(port=0, access_type="offline",
                                  prompt="consent")
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def load_service(secret_path: Path, token_path: Path, do_auth: bool):
    creds = load_creds(secret_path, token_path, do_auth)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def find_or_create_folder(service, name: str, parent_id: str) -> str:
    q = (f"mimeType='application/vnd.google-apps.folder' "
         f"and name='{name}' and '{parent_id}' in parents and trashed=false")
    res = service.files().list(q=q, spaces="drive",
                               fields="files(id,name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]}
    created = service.files().create(body=body, fields="id").execute()
    return created["id"]


def find_file_in_folder(service, name: str, folder_id: str) -> str | None:
    q = f"name='{name}' and '{folder_id}' in parents and trashed=false"
    res = service.files().list(q=q, spaces="drive", fields="files(id)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None


def make_shareable(service, file_id: str) -> str:
    perm = {"type": "anyone", "role": "reader"}
    service.permissions().create(fileId=file_id, body=perm).execute()
    return f"https://drive.google.com/file/d/{file_id}/view"


def convert_target_mime(name: str, convert: bool) -> str | None:
    """Tra ve Google native mimeType de convert, hoac None neu khong convert."""
    if not convert:
        return None
    low = name.lower()
    if low.endswith((".docx", ".doc")):
        return "application/vnd.google-apps.document"
    if low.endswith((".xlsx", ".xls", ".csv")):
        return "application/vnd.google-apps.spreadsheet"
    if low.endswith((".pptx", ".ppt")):
        return "application/vnd.google-apps.presentation"
    return None


def upload(file_path: Path, secret_path: Path, token_path: Path,
           do_auth: bool, parent_id: str, subfolder: str | None,
           share: bool, overwrite: bool, convert: bool) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"File khong ton tai: {file_path}")

    service = load_service(secret_path, token_path, do_auth)

    # parent_id = root folder. Default "root" = My Drive root.
    current_parent = parent_id

    if subfolder:
        for part in subfolder.replace("\\", "/").split("/"):
            part = part.strip()
            if part:
                current_parent = find_or_create_folder(service, part, current_parent)

    name = file_path.name
    target_mime = convert_target_mime(name, convert)

    # Khi convert, ten file khong nen giu .docx (Drive auto strip, nhun dat cu the)
    upload_name = name if not target_mime else name

    target_id: str | None = None
    if overwrite:
        target_id = find_file_in_folder(service, name, current_parent)

    if target_mime:
        media = MediaFileUpload(str(file_path),
                                mimetype=_source_mime(name),
                                resumable=True)
    else:
        media = MediaFileUpload(str(file_path), resumable=True)

    if target_id:
        service.files().update(fileId=target_id, media_body=media,
                                supportsAllDrives=False).execute()
        file_id = target_id
    else:
        body: dict = {"name": upload_name, "parents": [current_parent]}
        if target_mime:
            body["mimeType"] = target_mime
        created = service.files().create(body=body, media_body=media,
                                         fields="id").execute()
        file_id = created["id"]

    link = (make_shareable(service, file_id) if share
            else f"https://drive.google.com/file/d/{file_id}/view")

    # Native doc/sheet/presentation dung link khac
    if target_mime == "application/vnd.google-apps.document":
        link = (f"https://docs.google.com/document/d/{file_id}/edit"
                if share else f"https://docs.google.com/document/d/{file_id}/edit")
    elif target_mime == "application/vnd.google-apps.spreadsheet":
        link = f"https://docs.google.com/spreadsheets/d/{file_id}/edit"
    elif target_mime == "application/vnd.google-apps.presentation":
        link = f"https://docs.google.com/presentation/d/{file_id}/edit"

    return {
        "file_id": file_id,
        "link": link,
        "folder": subfolder or "/",
        "name": name,
        "converted_to": target_mime,
    }


def _source_mime(name: str) -> str:
    low = name.lower()
    if low.endswith(".docx"):
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if low.endswith(".xlsx"):
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if low.endswith(".pptx"):
        return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    if low.endswith(".csv"):
        return "text/csv"
    return "application/octet-stream"


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload file len Drive qua OAuth")
    parser.add_argument("file", nargs="?", help="Duong dan file can upload")
    parser.add_argument("--folder", default=None,
                        help="Subfolder (a/b/c) duoi parent")
    parser.add_argument("--parent", default="root",
                        help="Folder ID parent (default 'root' = My Drive root)")
    parser.add_argument("--share", action="store_true",
                        help="Set anyone-with-link viewer")
    parser.add_argument("--overwrite", action="store_true",
                        help="Ghi de neu file trung ten")
    parser.add_argument("--convert", action="store_true",
                        help="Convert Office sang native Google Doc/Sheet/Presentation")
    parser.add_argument("--auth", action="store_true",
                        help="Lan dau: mo browser de consent, tao token.json")
    args = parser.parse_args()

    secret_env = os.environ.get("DUKICK_OAUTH_SECRET")
    token_env = os.environ.get("DUKICK_OAUTH_TOKEN")
    secret_path = Path(secret_env) if secret_env else DEFAULT_SECRET
    token_path = Path(token_env) if token_env else DEFAULT_TOKEN

    if args.auth:
        try:
            load_creds(secret_path, token_path, do_auth=True)
            print(json.dumps({"auth": "OK", "token": str(token_path)},
                             ensure_ascii=False))
            return 0
        except Exception as exc:  # noqa: BLE001
            print(json.dumps({"error": str(exc)}, ensure_ascii=False),
                  file=sys.stderr)
            return 1

    if not args.file:
        print(json.dumps({"error": "Thieu file path. Dung --auth lan dau."},
                         ensure_ascii=False), file=sys.stderr)
        return 1

    try:
        result = upload(Path(args.file), secret_path, token_path, args.auth,
                        args.parent, args.folder, args.share, args.overwrite,
                        args.convert)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001 - hook safe
        print(json.dumps({"error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
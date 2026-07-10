"""
shared/upload_to_drive.py — Upload files to Google Drive with auto-convert native + auto-public.

Usage:
    from shared.upload_to_drive import upload_file
    result = upload_file(r"C:\\path\\to\\file.docx", make_public=True)
"""

import json
import os
import urllib.request
from shared.gauth import get_auth_header

UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
CONVERT_MAP = {
    ".docx": {"upload": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
              "target": "application/vnd.google-apps.document"},
    ".xlsx": {"upload": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
              "target": "application/vnd.google-apps.spreadsheet"},
    ".pptx": {"upload": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
              "target": "application/vnd.google-apps.presentation"},
    ".pdf":  {"upload": "application/pdf", "target": None},
}

def _set_public_permission(file_id):
    """Set anyone with link can edit."""
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions"
    body = json.dumps({"role": "writer", "type": "anyone"}).encode()
    req = urllib.request.Request(url, data=body, headers={**get_auth_header(), "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=30)
    except Exception:
        pass  # silently ignore if already public

def upload_file(local_path, folder_id=None, convert=True, make_public=True):
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Not found: {local_path}")
    ext = os.path.splitext(local_path)[1].lower()
    mapping = CONVERT_MAP.get(ext, {"upload": "application/octet-stream", "target": None})
    filename = os.path.basename(local_path)
    with open(local_path, "rb") as f:
        file_bytes = f.read()
    meta = {"name": filename}
    if convert and mapping["target"]:
        meta["mimeType"] = mapping["target"]
    if folder_id:
        meta["parents"] = [folder_id]
    boundary = "----DukickBoundary42"
    headers = get_auth_header()
    headers["Content-Type"] = f"multipart/related; boundary={boundary}"
    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(meta)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: {mapping['upload']}\r\n\r\n"
    ).encode() + file_bytes + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(UPLOAD_URL, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
    file_id = result["id"]
    if make_public:
        _set_public_permission(file_id)
    detail_req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=id,name,mimeType,webViewLink",
        headers=get_auth_header()
    )
    with urllib.request.urlopen(detail_req, timeout=30) as detail_resp:
        return json.loads(detail_resp.read().decode())

def create_folder(name, parent_folder_id=None):
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_folder_id:
        meta["parents"] = [parent_folder_id]
    req = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/files",
        data=json.dumps(meta).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def list_files(query="", page_size=50):
    url = f"https://www.googleapis.com/drive/v3/files?pageSize={page_size}&fields=files(id,name,mimeType,webViewLink)"
    if query:
        url += f"&q={urllib.request.quote(query)}"
    req = urllib.request.Request(url, headers=get_auth_header())
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    print("Google Drive Upload module loaded.")

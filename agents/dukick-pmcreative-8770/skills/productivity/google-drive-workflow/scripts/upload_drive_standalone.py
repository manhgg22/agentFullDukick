import sys, json, os, urllib.request, base64

# CONFIGURE THIS for the target agent
shared_dir = r"C:\DuKickAgent\agents\dukick-pmcreative-8770\shared"
sys.path.insert(0, shared_dir)
from gauth import get_auth_header

# Agent folder mapping — copy from drive_config.py if import fails
FOLDER_MAP = {
    "dukick-pmcreative-8770": "10rT0BK4K6N6vwVP641ezJE9w75TeLKlL",
}

def upload_to_drive(file_path, agent_name="dukick-pmcreative-8770", convert=True, make_public=True):
    folder_id = FOLDER_MAP.get(agent_name)
    if not folder_id:
        raise ValueError(f"Agent {agent_name} not in FOLDER_MAP")
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    
    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    mapping = {
        ".docx": {"upload": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  "target": "application/vnd.google-apps.document"},
        ".xlsx": {"upload": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                  "target": "application/vnd.google-apps.spreadsheet"},
        ".pptx": {"upload": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                  "target": "application/vnd.google-apps.presentation"},
        ".pdf":  {"upload": "application/pdf", "target": None},
    }.get(ext, {"upload": "application/octet-stream", "target": None})
    
    meta = {"name": filename, "parents": [folder_id]}
    if convert and mapping["target"]:
        meta["mimeType"] = mapping["target"]
    
    boundary = "----DukickBoundary42"
    headers = get_auth_header()
    headers["Content-Type"] = f"multipart/related; boundary={boundary}"
    
    body_parts = [
        f"--{boundary}",
        "Content-Type: application/json; charset=UTF-8",
        "",
        json.dumps(meta, ensure_ascii=False),
        f"--{boundary}",
        f"Content-Type: {mapping['upload']}",
        "Content-Transfer-Encoding: base64",
        "",
        base64.b64encode(file_bytes).decode(),
        f"--{boundary}--",
        ""
    ]
    
    req_body = "\r\n".join(body_parts).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=req_body, headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.load(resp)
    
    file_id = result.get("id")
    if make_public and file_id:
        perm_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions"
        perm_body = json.dumps({"role": "writer", "type": "anyone"}).encode()
        perm_req = urllib.request.Request(perm_url, data=perm_body,
            headers={**get_auth_header(), "Content-Type": "application/json"})
        try:
            urllib.request.urlopen(perm_req, timeout=30)
        except Exception:
            pass
    
    return {
        "file_id": file_id,
        "link": f"https://docs.google.com/document/d/{file_id}/edit" if mapping["target"] == "application/vnd.google-apps.document" else f"https://drive.google.com/file/d/{file_id}/view",
        "result": result
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python upload_drive_standalone.py <file_path> [agent_name]")
        sys.exit(1)
    result = upload_to_drive(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "dukick-pmcreative-8770")
    print(json.dumps(result, indent=2, ensure_ascii=False))

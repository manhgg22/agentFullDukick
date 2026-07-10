---
name: google-drive-ops
description: |
  Google Drive API integration for Hermes agents — OAuth2 setup, token auto-refresh,
  file upload with native conversion, public-permission management, and multi-agent
  shared-library distribution. Built for Dukick ecosystem.
triggers:
  - "connect google drive"
  - "upload to drive"
  - "google docs api"
  - "google sheets api"
  - "oauth2 google"
  - "public file on drive"
---

# Google Drive Ops for Dukick Agents

## 1. OAuth2 Flow (First-Time Setup)

### 1.1 Prerequisites
- Google Cloud Project with Drive API + Docs API + Sheets API enabled.
- OAuth2 **Desktop** client credentials (`client_secret_*.json`).
- `redirect_uris` must include `http://localhost:8499/` (or whatever port the auth callback server uses).

### 1.2 Get Authorization Code
Build the auth URL (replace `CLIENT_ID` and `REDIRECT_URI`):

```
https://accounts.google.com/o/oauth2/auth?
  client_id=<CLIENT_ID>
  &redirect_uri=http://localhost:8499/
  &scope=https://www.googleapis.com/auth/documents%20https://www.googleapis.com/auth/spreadsheets%20https://www.googleapis.com/auth/drive
  &response_type=code
  &access_type=offline
  &prompt=consent
```

User opens in browser → logs in with Dukick account → approves → copy `code=` from redirected URL.

**Code is one-time use and expires in ~5 minutes.**

### 1.3 Exchange Code for Tokens

**CRITICAL PITFALL:** `execute_code` redacts secrets/token values in stdout. If you print tokens, they get masked (`ya29.a...0206`) and the saved file will contain the masked garbage, not real tokens.

**Safe approaches:**
1. **Write tokens directly to file** inside `execute_code` without printing them.
2. **Use terminal script** (`python script.py`) where stdout redaction does not affect file writes.

Example safe exchange script (save as `exchange_token.py`):

```python
import urllib.request, urllib.parse, json, os

CRED_JSON = r"C:\path\to\client_secret_*.json"
CODE = os.environ.get("GAUTH_CODE", "")
SHARED_DIR = r"C:\DuKickAgent\agents\<AGENT>\shared"

with open(CRED_JSON) as f:
    creds = json.load(f)["installed"]

post = urllib.parse.urlencode({
    "code": CODE,
    "client_id": creds["client_id"],
    "client_secret": creds["client_secret"],
    "redirect_uri": "http://localhost:8499/",
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request("https://oauth2.googleapis.com/token", data=post,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
with urllib.request.urlopen(req, timeout=30) as resp:
    tokens = json.loads(resp.read().decode())

os.makedirs(SHARED_DIR, exist_ok=True)
with open(os.path.join(SHARED_DIR, "gauth_tokens.json"), "w") as f:
    json.dump(tokens, f, indent=2)
```

### 1.4 Token File Structure (`gauth_tokens.json`)

```json
{
  "access_token": "ya29.a...",
  "refresh_token": "1//0ey...",
  "token_type": "Bearer",
  "expires_in": 3599,
  "scope": "https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/spreadsheets"
}
```

## 2. Auth Library (`gauth.py`)

Shared module every agent imports. Must live in `shared/gauth.py` with `shared/__init__.py`.

Key functions:
- `get_access_token()` — reads token file, auto-refreshes if >50 min old.
- `get_auth_header()` — returns `{"Authorization": "Bearer <token>"}`.
- `test_connection()` — calls Drive `about?fields=user` to verify.

Refresh logic uses `token_uri = https://oauth2.googleapis.com/token` with `refresh_token` + `client_secret`.

## 3. Upload to Drive (`upload_to_drive.py`)

### Native Conversion Map
| Local Ext | Upload MIME | Target (Native) |
|---|---|---|
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `application/vnd.google-apps.document` |
| `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | `application/vnd.google-apps.spreadsheet` |
| `.pptx` | `application/vnd.openxmlformats-officedocument.presentationml.presentation` | `application/vnd.google-apps.presentation` |
| `.pdf` | `application/pdf` | No conversion |

### Auto-Public Permission
Default `make_public=True` on `upload_file()`. After upload, calls:

```python
POST https://www.googleapis.com/drive/v3/files/{file_id}/permissions
Body: {"role": "writer", "type": "anyone"}
```

This grants **anyone with link can edit**.

### Critical Pitfall: execute_code Redaction
`execute_code` redacts secrets in stdout using regex patterns. **Tokens printed to stdout get masked** (e.g. `ya29.a...0206` instead of real value). If you then save that masked output to a file, the token file becomes useless.

**Fix:** In `execute_code`, write tokens directly to file via `open().write()` **without printing them first**. Or use terminal script execution where stdout redaction does not affect file writes.

## 4. Docs & Sheets Ops

- `docs_ops.py` — `create_doc`, `append_text`, `insert_heading`, `read_doc`, `replace_text`
- `sheets_ops.py` — `create_sheet`, `write_range`, `read_range`, `append_rows`, `clear_range`

All use `shared.gauth.get_auth_header()`.

## 5. Multi-Agent Folder Structure (1 Gmail → N Department Folders)

When multiple agents share one Google account but need separate workspaces:

1. **Create N folders on Drive** (one per agent/department):
   ```
   01-Truyền Thông/
   02-Kế Toán/
   03-PM/
   04-PM Creative/
   05-Tổng/
   06-HR/
   ```

2. **Hardcode folder_id per agent** in `shared/drive_config.py`:
   ```python
   FOLDER_MAP = {
       "dukick-truyenthong-8768": "1tDfaVW9a3zqACLgyGa1n1YZMHo4GYRZD",
       "dukick-ketoan-8771": "18NUJCy1XraNWJkn_iIcT8qyC4CEaCF6r",
       # ...etc
   }
   def get_folder_id(agent_name):
       return FOLDER_MAP.get(agent_name)
   ```

3. **Usage in upload:**
   ```python
   from shared.drive_config import get_folder_id
   from shared.upload_to_drive import upload_file
   folder_id = get_folder_id("dukick-truyenthong-8768")
   result = upload_file(path, folder_id=folder_id)
   ```

## 6. Multi-Agent Distribution Pattern

When a shared library must be deployed to N agents:

1. Build in **source agent** `shared/`.
2. Copy files with Python script (avoids bash path issues on Windows):

```python
import shutil, os
source = r"C:\DuKickAgent\agents\SOURCE\shared"
agents = [r"C:\DuKickAgent\agents\A", r"C:\DuKickAgent\agents\B", ...]
files = ["gauth.py", "gauth_tokens.json", "upload_to_drive.py",
         "docs_ops.py", "sheets_ops.py", "drive_config.py", "__init__.py",
         "client_secret.json"]  # see §7
for agent in agents:
    os.makedirs(os.path.join(agent, "shared"), exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(source, f), os.path.join(agent, "shared", f))
```

3. Ensure `shared/__init__.py` exists in every agent so `from shared.gauth import ...` works.

## 7. Pitfall: Uploaded File Name Corrupts client_secret Discovery

When a user uploads `client_secret_*.json` via chat, the saved filename may get a `doc_` prefix (e.g. `doc_52d046713e7d_client_secret_5538...apps.googleusercontent.com.json`).

`gauth._load_creds()` searches for files `startswith("client_secret")` — this prefixed name does **not** match, causing:
```
RuntimeError: CLIENT_SECRET chưa được cấu hình.
```

**Fix:** Rename uploaded file to `client_secret.json` (or any clean name matching the expected pattern) before distributing to agents:
```python
import os, glob
for f in os.listdir(shared_dir):
    if "client_secret" in f and f.endswith(".json") and f != "client_secret.json":
        os.rename(os.path.join(shared_dir, f), os.path.join(shared_dir, "client_secret.json"))
```

## 6. Verification Checklist

- [ ] Tokens saved without redaction/masking
- [ ] `shared/__init__.py` present
- [ ] `test_connection()` returns Dukick Editor account
- [ ] Upload returns `webViewLink`
- [ ] Public permission returns HTTP 200
- [ ] All target agents have identical `shared/` contents

## References

- `references/oauth-endpoints.md` — Google OAuth2 endpoint details & scope strings
- `scripts/exchange_token.py` — Standalone token exchange script
- `scripts/copy_shared_to_agents.py` — Multi-agent distribution script
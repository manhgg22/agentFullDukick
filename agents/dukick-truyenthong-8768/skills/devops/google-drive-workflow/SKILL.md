---
name: google-drive-workflow
description: Complete Google Drive API workflow for Hermes agents — OAuth setup, token exchange, multi-agent shared-folder sync, native file conversion (docx→Doc, xlsx→Sheet, pptx→Slides), auto-public permissions, and Drive folder management.
trigger: Whenever setting up Google Drive integration, uploading files to Drive, managing Drive folders, or syncing Drive across multiple Hermes agents.
---

# Google Drive Workflow for Hermes Agents

## 1. Prerequisites
- A Google Cloud project with OAuth 2.0 Desktop app credentials
- `client_secret_<id>.apps.googleusercontent.com.json`
- Mail Dukick (or target Google account) signed in on the same machine

## 2. OAuth Token Exchange

**⚠️ CRITICAL PITFALL:** `execute_code` redacts secrets in stdout. Never rely on printing tokens.

### Option A: Terminal script (recommended)
Write the exchange script to disk first, then run via `terminal()`.

```python
import urllib.request, urllib.parse, json, os

CRED_PATH = r"path/to/client_secret.json"
CODE = os.environ.get("GAUTH_CODE")  # set before running
REDIRECT_URI = "http://localhost:8499/"

with open(CRED_PATH) as f:
    creds = json.load(f)

CLIENT_ID = creds["installed"]["client_id"]
CLIENT_SECRET=creds[...data = urllib.parse.urlencode({
    "code": CODE, "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET, "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
with urllib.request.urlopen(req, timeout=30) as resp:
    tokens = json.loads(resp.read().decode())

# Save directly — never print
with open("gauth_tokens.json", "w") as f:
    json.dump(tokens, f, indent=2)
```

### Option B: Interactive browser flow
1. Build auth URL with `redirect_uri`, `scope` (drive + docs + spreadsheets), `access_type=offline`, `prompt=consent`
2. User opens in browser → allows → copies `code=...` from redirect URL
3. Exchange via terminal script above

## 3. Multi-Agent Sync Pattern

Each Hermes agent has its own working directory. To share Drive tokens + libs across agents:

```bash
# Copy shared/ folder to all agents
for agent in agent-1 agent-2 agent-3; do
  mkdir -p "$AGENTS_DIR/$agent/shared"
  cp shared/gauth.py shared/gauth_tokens.json shared/upload_to_drive.py \
     shared/docs_ops.py shared/sheets_ops.py shared/drive_config.py \
     shared/client_secret.json "$AGENTS_DIR/$agent/shared/"
  touch "$AGENTS_DIR/$agent/shared/__init__.py"
done
```

**Convention:** `shared/__init__.py` required for `from shared.xxx import`.

## 4. Auth Lib (`gauth.py`)

Must support:
- Reading `client_secret.json` from `shared/` (fallback to env)
- Auto-refresh via `refresh_token` when `access_token` expires (~50 min)
- `get_access_token()` → returns valid token
- `get_auth_header()` → `{"Authorization": "Bearer <token>"}`

Pitfall: if `client_secret.json` has a long filename (e.g. prefixed with `doc_...`), rename to `client_secret.json` or update `_load_creds()` to match any `*client_secret*.json`.

## 5. Upload with Native Conversion + Auto-Public

```python
from shared.upload_to_drive import upload_file

result = upload_file(
    r"path/to/file.docx",
    folder_id="YOUR_FOLDER_ID",
    convert=True,      # .docx → Google Docs native
    make_public=True,  # anyone with link can edit
)
print(result["webViewLink"])
```

Conversion map:
| Ext | Upload MIME | Target MIME |
|---|---|---|
| .docx | `wordprocessingml.document` | `google-apps.document` |
| .xlsx | `spreadsheetml.sheet` | `google-apps.spreadsheet` |
| .pptx | `presentationml.presentation` | `google-apps.presentation` |
| .pdf | `application/pdf` | (no conversion) |

## 6. Folder Structure per Agent

Recommended structure under one Gmail Drive:

```
Dukick Workspace/
├── 01-Truyền Thông/
├── 02-Kế Toán/
├── 03-PM/
├── 04-PM Creative/
├── 05-Tổng/
├── 06-HR/
```

Use `drive_config.py` to hardcode `folder_id` per agent:

```python
FOLDER_MAP = {
    "agent-name-1": "FOLDER_ID_1",
    "agent-name-2": "FOLDER_ID_2",
}
```

## 7. Setting Public Permissions

```python
import urllib.request, json
from shared.gauth import get_auth_header

def set_public(file_or_folder_id, role="reader"):  # or "writer"
    url = f"https://www.googleapis.com/drive/v3/files/{file_or_folder_id}/permissions"
    body = json.dumps({"role": role, "type": "anyone"}).encode()
    req = urllib.request.Request(url, data=body,
        headers={**get_auth_header(), "Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=30)
```

## 8. Files & Scripts in This Skill
- `scripts/exchange_token.py` — OAuth code → tokens (terminal-safe)
- `scripts/upload_to_drive.py` — Upload module with convert + public
- `scripts/gauth.py` — Auth lib with auto-refresh
- `scripts/drive_config.py` — Per-agent folder ID mapping
- `references/agent_folder_ids.json` — Example folder IDs for Dukick agents

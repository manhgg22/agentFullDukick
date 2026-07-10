---
name: google-workspace-integration
description: |
  OAuth2 authentication and API operations for Google Workspace (Drive, Docs, Sheets, Slides).
  Covers desktop-app OAuth flow, authorization-code exchange, token storage, auto-refresh,
  and the critical execute_code stdout-redaction pitfall that corrupts secrets.
---

# Google Workspace Integration

## When to use
- Connecting to Google Drive, Docs, Sheets, or Slides APIs programmatically.
- Setting up OAuth2 desktop-client flow for a new project or agent profile.
- Refreshing expired access tokens or re-authing after credential rotation.

## Prerequisites
- Google Cloud project with the **Google Drive API**, **Docs API**, and/or **Sheets API** enabled.
- OAuth 2.0 credentials of type **Desktop app** downloaded (`client_secret_*.json`).
- At least one **Authorized redirect URI** registered in the console that matches your local callback (e.g. `http://localhost:8499/`).

## OAuth2 Desktop Flow

### 1. Build the authorization URL
```
https://accounts.google.com/o/oauth2/auth
  ?client_id=<CLIENT_ID>
  &redirect_uri=<REDIRECT_URI>
  &scope=<SPACE_SEPARATED_SCOPES>
  &response_type=code
  &access_type=offline
  &prompt=consent
```

Common scopes:
| API | Scope |
|-----|-------|
| Drive | `https://www.googleapis.com/auth/drive` |
| Docs | `https://www.googleapis.com/auth/documents` |
| Sheets | `https://www.googleapis.com/auth/spreadsheets` |
| Slides | `https://www.googleapis.com/auth/presentations` |

### 2. User authorizes in browser
Open the URL while logged into the target Google account. After clicking **Allow**, copy the `code` query parameter from the redirected `localhost` URL.

> **Authorization codes are one-time-use and expire in ~5 minutes.**

### 3. Exchange code for tokens
POST `application/x-www-form-urlencoded` to `https://oauth2.googleapis.com/token`:
- `code`
- `client_id`
- `client_secret`
- `redirect_uri` — must match the registered URI **exactly** (port matters).
- `grant_type=authorization_code`

Response contains `access_token`, `refresh_token`, `expires_in`, `token_type`, `scope`.

### 4. Store tokens
Save the JSON response to a file (e.g. `shared/gauth_tokens.json`).

---

## ⚠️ CRITICAL PITFALL: execute_code stdout redaction

Hermes redacts values that look like secrets or tokens from `execute_code` stdout. **If you `print()` an access token or refresh token, the redacted placeholder (e.g. `ya29.a...0206`) gets written to any file or variable derived from that stdout**, corrupting the real credential.

### Safe patterns

| Approach | How |
|----------|-----|
| **Write directly to file** | In the Python script, call `json.dump(tokens, open(path,"w"))` and never `print(tokens)`. |
| **Use terminal script** | Write a standalone `.py` script to disk, then run it via `terminal()`. Terminal output is NOT redacted. |
| **Read credentials from file** | Store `client_secret` in a JSON file on disk; the script reads it at runtime instead of embedding it in code. |

### Unsafe pattern (DO NOT)
```python
# BAD: stdout gets redacted, file now contains placeholder tokens
result = json.dumps(tokens)
print(result)                      # redacted here
with open("tokens.json","w") as f:
    f.write(result)                # also redacted
```

---

## Token Refresh

When `access_token` expires (~1 hour), exchange the `refresh_token` without user interaction:

POST to `https://oauth2.googleapis.com/token`:
- `refresh_token`
- `client_id`
- `client_secret`
- `grant_type=refresh_token`

Response returns a new `access_token` and `expires_in`.

---

## Verification

Quick health-check after exchange:
```
GET https://www.googleapis.com/drive/v3/about?fields=user
Authorization: Bearer <access_token>
```

A successful response confirms the account, display name, and email address.

---

## Dukick Project Convention

Store reusable auth logic under a `shared/` directory:

```
shared/
  __init__.py           # Makes shared/ a Python package for import
  gauth.py              # Read tokens from file, auto-refresh if expired
  gauth_tokens.json     # Stored tokens (add to .gitignore)
  upload_to_drive.py    # Upload + convert to native format
  docs_ops.py           # Native Google Docs CRUD
  sheets_ops.py         # Native Google Sheets CRUD
```

## Multi-Agent Token Distribution

When multiple Hermes agents need the same Google account:

1. **Exchange tokens once** in the source agent's `shared/` directory
2. **Copy the entire `shared/` folder** (including `gauth_tokens.json`) to every target agent
3. **Each agent gets its own token copy** so mtime-based refresh logic works independently
4. **Add `sys.path.insert(0, agent_root)** when importing from scripts outside the agent directory

```python
import shutil, os

source = r"C:\DuKickAgent\agents\source-agent\shared"
targets = [r"C:\DuKickAgent\agents\agent-1", ...]
files = ["gauth.py", "gauth_tokens.json", "upload_to_drive.py",
         "docs_ops.py", "sheets_ops.py", "__init__.py"]

for agent in targets:
    dst = os.path.join(agent, "shared")
    os.makedirs(dst, exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(source, f), os.path.join(dst, f))
```

## Core Module Reference

### gauth.py

| Function | Purpose |
|----------|---------|
| `get_access_token()` | Returns valid access_token (auto-refresh if >50 min old) |
| `get_auth_header()` | Returns `{"Authorization": "Bearer <token>"}` |
| `test_connection()` | Calls Drive `about` API, returns user info |

Auto-refresh logic: checks file mtime; if >3000s (50 min), uses `refresh_token` to get new `access_token`.

### upload_to_drive.py

| Function | Purpose |
|----------|---------|
| `upload_file(path, folder_id=None, convert=True)` | Upload file; auto-convert docx/xlsx/pptx to native |
| `create_folder(name, parent_folder_id=None)` | Create Drive folder |
| `list_files(query="", page_size=50)` | List Drive files |

**Native Convert Mapping:**
| Extension | Upload MIME | Target MIME (convert) |
|-----------|-------------|----------------------|
| .docx | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `application/vnd.google-apps.document` |
| .xlsx | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | `application/vnd.google-apps.spreadsheet` |
| .pptx | `application/vnd.openxmlformats-officedocument.presentationml.presentation` | `application/vnd.google-apps.presentation` |

### docs_ops.py

| Function | Purpose |
|----------|---------|
| `create_doc(title)` | Create new Google Doc |
| `read_doc(doc_id)` | Read full document content |
| `append_text(doc_id, text, end_of_doc=True)` | Append text to end/start |
| `insert_heading(doc_id, text, level=1)` | Insert HEADING_1/2/3 |
| `replace_text(doc_id, old, new)` | Replace all occurrences |

### sheets_ops.py

| Function | Purpose |
|----------|---------|
| `create_sheet(title)` | Create new Google Sheet |
| `read_range(id, "Sheet1!A1:C10")` | Read cell range |
| `write_range(id, range, values, value_input_option="RAW")` | Write to range |
| `append_rows(id, sheet_name, rows)` | Append rows to bottom |
| `clear_range(id, range)` | Clear cell range |
| `rename_sheet(id, new_title)` | Rename spreadsheet |

## References
- See `references/oauth-exchange-script.py` for a standalone, redaction-safe exchange script.

# Reading Google Docs via Docs API

## Problem
Defuddle and WebFetch cannot extract content from `docs.google.com` URLs because Google Docs requires OAuth 2.0 authentication.

## Solution
Use the environment's pre-configured Google auth (`shared/gauth.py`) via `execute_code` to call the Docs API v1.

## Inline Code Pattern (no `shared` import via execute_code)

```python
import sys, json, os, urllib.request
# Point to agent's shared/ directory
shared_dir = r"C:\DuKickAgent\agents\dukick-pmcreative-8770\shared"
sys.path.insert(0, shared_dir)
from gauth import get_auth_header

def extract_doc_text(doc_id):
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}"
    req = urllib.request.Request(url, headers=get_auth_header())
    with urllib.request.urlopen(req, timeout=30) as resp:
        doc = json.load(resp)
    
    def get_text(elements):
        out = ""
        for el in elements:
            tr = el.get("textRun")
            if tr:
                out += tr.get("content", "")
        return out
    
    lines = []
    for item in doc.get("body", {}).get("content", []):
        if "paragraph" in item:
            text = get_text(item["paragraph"].get("elements", []))
            if text:
                lines.append(text)
        elif "table" in item:
            for row in item["table"].get("tableRows", []):
                row_texts = []
                for cell in row.get("tableCells", []):
                    cell_texts = []
                    for c in cell.get("content", []):
                        if "paragraph" in c:
                            t = get_text(c["paragraph"].get("elements", []))
                            if t:
                                cell_texts.append(t.strip())
                    row_texts.append(" | ".join(cell_texts))
                lines.append(" | ".join(row_texts))
    return "".join(lines)

# Usage
DOC_ID = "1yPZM7oRsO2Sk58MpjXYpMPkRfY0cIfjNyzz9y8zeAcQ"
text = extract_doc_text(DOC_ID)
print(text)
```

## Key Notes
- `get_auth_header()` handles auto-refresh of the access token.
- Token file: `shared/gauth_tokens.json` (pre-authorized).
- Client credentials: `shared/client_secret.json`.
- Agent folder IDs: `shared/drive_config.py` → `FOLDER_MAP`.

## Why not `from shared.gauth import ...` in execute_code?

`execute_code` runs in a fresh temp directory with `sys.path` not including `CWD/shared/`. Direct `from shared.gauth` fails with `ModuleNotFoundError`. Always `sys.path.insert(0, shared_dir)` before importing, or inline the auth code.

# Google Drive Module — Internal Structure

Discovered during FISV Brand Film session (2026-07-09).

## Module Files
```
C:\DuKickAgent\agents\dukick-pmcreative-8770\shared\
├── upload_to_drive.py   # Upload, convert, permission APIs
├── drive_config.py      # Agent → folder_id mapping
└── gauth.py             # Auth header (credentials from .env)
```

## Agent Folder IDs (FOLDER_MAP)
| Agent | Folder ID |
|-------|-----------|
| dukick-truyenthong-8768 | 1tDfaVW9a3zqACLgyGa1n1YZMHo4GYRZD |
| dukick-ketoan-8771 | 18NUJCy1XraNWJkn_iIcT8qyC4CEaCF6r |
| dukick-pm-8769 | 10PuVkvshc5jo-fK8wow9QVJ0T5T8qOGi |
| **dukick-pmcreative-8770** | **10rT0BK4K6N6vwVP641ezJE9w75TeLKlL** |
| dukick-tong-8767 | 17kl9Nzas4rUvQybFLzhPjFmhWAhS9USk |
| hermes-hr-8772 | 1v1dJH_JKTBb2cSnmLCRLbqVe0nWGvcXN |

## API Endpoints Used
- `POST https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart` — upload
- `POST https://www.googleapis.com/drive/v3/files/{id}/permissions` — set public
- `GET https://www.googleapis.com/drive/v3/files/{id}?fields=id,name,mimeType,webViewLink` — get details

## Markdown → DOCX Conversion Options
1. **python-docx** (available in venv): basic conversion, headings, paragraphs, bold
2. **pandoc** (if installed): higher fidelity table rendering
3. **Fallback**: upload raw `.md` with `convert=False` (kept as raw text in Drive)

## Permission Behavior
- `make_public=True` → role `"writer"`, type `"anyone"` (editable by link)
- If user wants view-only, call `_set_public_permission` manually with `"reader"` role, or set `make_public=False`

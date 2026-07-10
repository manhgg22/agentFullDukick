---
name: google-drive-workflow
description: Upload and share files via Google Drive using the built-in dukick shared modules. Covers file conversion, public-permission links, and per-agent folder routing.
category: productivity
---

# Google Drive Workflow

## When to Use
Use this skill when the user asks to upload, save, or share a file/document to Google Drive, Google Docs, or requests a shareable link from the agent environment.

## Prerequisites
- The agent environment contains `shared/upload_to_drive.py` and `shared/drive_config.py`.
- Drive credentials are configured in the agent's `.env` (consumed via `shared.gauth`).
- The current agent has a mapped folder ID in `shared.drive_config.FOLDER_MAP`.

## Workflow

1. **Prepare the file locally**
   - Convert `.md` to `.docx` (or `.pdf`) before uploading — the Drive uploader does not auto-convert Markdown.
   - For `.docx`, `.xlsx`, `.pptx`, `.pdf`, set `convert=True` to turn them into native Google formats.

2. **Import the upload module**
   ```python
   from shared.drive_config import get_folder_id
   from shared.upload_to_drive import upload_file
   ```

3. **Get the destination folder ID**
   ```python
   folder_id = get_folder_id("dukick-pmcreative-8770")  # use current agent name
   ```

4. **Upload with conversion + public link**
   ```python
   result = upload_file(
       local_path=r"C:\path\to\file.docx",
       folder_id=folder_id,
       convert=True,        # Office/PDF → Google format
       make_public=True     # "Anyone with the link" can edit
   )
   link = result["webViewLink"]
   ```

## Supported Auto-Conversions
| Extension | Upload MIME | Converts To |
|-----------|-------------|-------------|
| `.docx`   | Word        | Google Docs |
| `.xlsx`   | Excel       | Google Sheets |
| `.pptx`   | PowerPoint  | Google Slides |
| `.pdf`    | PDF         | PDF (no conversion) |

## Pitfalls
- **Markdown must be converted first.** The uploader treats `.md` as raw text. Use `python-docx` or `pandoc` to convert to `.docx` before calling `upload_file`.
- **Timeout:** The upload API has a 60-second timeout; very large files may need chunking or a different approach.
- **Permissions:** `make_public=True` sets the "writer" role. If the user only wants view access, set `make_public=False` and adjust permissions manually afterward.
- **Agent folder mapping:** If `get_folder_id` returns `FALLBACK_ID`, the current agent is not mapped in `drive_config.py`. Ask the user for the target folder ID or upload to root.
- **`execute_code` does NOT auto-include `shared/` in `sys.path`.** When running upload or auth code via `execute_code`, add `sys.path.insert(0, r"C:\DuKickAgent\agents\<agent>\shared")` before importing `shared.*` modules, or inline the code (import `gauth` directly, copy `FOLDER_MAP`, etc.) to avoid `ModuleNotFoundError: No module named 'shared'`.

## References
- `references/drive-module-structure.md` — Internal module paths, agent folder IDs, and API details discovered in sessions.

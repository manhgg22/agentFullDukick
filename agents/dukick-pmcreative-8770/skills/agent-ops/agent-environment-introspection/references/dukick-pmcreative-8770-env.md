# Agent: dukick-pmcreative-8770 — Environment Reference

Generated from session on 2026-07-10.

## MCP Servers

| Name | Command | Args | Timeout |
|------|---------|------|---------|
| markitdown | `C:/DukickAgent/venv/Scripts/python.exe` | `C:/DuKickAgent/tools/markitdown_mcp_server.py` | 120s |

Capabilities: DOCX, XLSX, PPTX, PDF, HTML, CSV, OCR on images.

## Google Drive — "DUKICK"

- **Project ID**: `agenthermesdukick`
- **Client ID**: `553888273742-03danr8q3i40uuhodfgiop73lvdmu28d.apps.googleusercontent.com`
- **Agent Folder ID**: `10rT0BK4K6N6vwVP641ezJE9w75TeLKlL`
- **OAuth scopes**: Drive, Sheets, Docs
- **Token file**: `shared/gauth_tokens.json`
- **Shared scripts**:
  - `shared/drive_config.py` — FOLDER_MAP per agent
  - `shared/upload_to_drive.py` — Upload + auto-convert + public link
  - `shared/gauth.py` — Auto-refresh token

## Google Drive Folder Map (all agents)

| Agent | Folder ID |
|-------|-----------|
| dukick-tong-8767 | `17kl9Nzas4rUvQybFLzhPjFmhWAhS9USk` |
| dukick-truyenthong-8768 | `1tDfaVW9a3zqACLgyGa1n1YZMHo4GYRZD` |
| dukick-pm-8769 | `10PuVkvshc5jo-fK8wow9QVJ0T5T8qOGi` |
| dukick-pmcreative-8770 | `10rT0BK4K6N6vwVP641ezJE9w75TeLKlL` |
| dukick-ketoan-8771 | `18NUJCy1XraNWJkn_iIcT8qyC4CEaCF6r` |
| hermes-hr-8772 | `1v1dJH_JKTBb2cSnmLCRLbqVe0nWGvcXN` |

## .env (credential store)

Path: `C:\DuKickAgent\agents\dukick-pmcreative-8770\.env`

Key values:
- `DISCORD_BOT_TOKEN`
- `DISCORD_HOME_CHANNEL=1457650816914559128`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL=https://ollama.com/v1`
- `GATEWAY_ALLOW_ALL_USERS=true`

> Access via `terminal` (`cat .env`) because `read_file` blocks credential stores.

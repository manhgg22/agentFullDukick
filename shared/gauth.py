"""Shared Google auth + service builder cho Drive/Docs/Sheets.

Doc: load_creds(), build_drive(), build_docs(), build_sheets().
Token auto-refresh neu het han.
"""
from __future__ import annotations

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Cho phep http localhost (oauthlib)
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
]

BASE = Path(__file__).resolve().parent / "gcp"
DEFAULT_SECRET = BASE / "client_secret.json"
DEFAULT_TOKEN = BASE / "token.json"


def load_creds() -> Credentials:
    """Load token, refresh neu het han. Raise neu chua consent."""
    secret_env = os.environ.get("DUKICK_OAUTH_SECRET")
    token_env = os.environ.get("DUKICK_OAUTH_TOKEN")
    secret_path = Path(secret_env) if secret_env else DEFAULT_SECRET
    token_path = Path(token_env) if token_env else DEFAULT_TOKEN

    if not token_path.exists():
        raise RuntimeError(
            f"Chua co token. Chay: python shared/oauth_manual_auth.py --url "
            f"roi --exchange <redirect_url> de consent."
        )
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if creds.valid:
        return creds
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
        return creds
    raise RuntimeError("Token invalid va khong refresh duoc. Consent lai.")


def build_drive():
    from googleapiclient.discovery import build
    return build("drive", "v3", credentials=load_creds(), cache_discovery=False)


def build_docs():
    from googleapiclient.discovery import build
    return build("docs", "v1", credentials=load_creds(), cache_discovery=False)


def build_sheets():
    from googleapiclient.discovery import build
    return build("sheets", "v4", credentials=load_creds(), cache_discovery=False)
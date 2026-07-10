"""Manual OAuth consent (2 len, khong can input interact).

Len 1 - sinh URL:
    python oauth_manual_auth.py --url

Len 2 - exchange code, save token:
    python oauth_manual_auth.py --exchange "<redirect_url_hoac_code>"

Flow:
1. --url  -> in auth URL -> mo o may/phone da login editor.dukick@gmail.com
2. Authorize -> Google redirect http://localhost/?code=... (trang KHONG load, binh thuong)
3. Copy NGUYEN URL address bar
4. --exchange "<URL_vua_copy>" -> save shared/gcp/token.json

Env:
    DUKICK_OAUTH_SECRET  duong dan client_secret.json (default shared/gcp/client_secret.json)
    DUKICK_OAUTH_TOKEN   duong dan token.json (default shared/gcp/token.json)
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Cho phep http localhost (oauthlib chan http mac dinh)
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
]
BASE = Path(__file__).resolve().parent / "gcp"
DEFAULT_SECRET = BASE / "client_secret.json"
DEFAULT_TOKEN = BASE / "token.json"


def make_flow(secret_path: Path):
    if not secret_path.exists():
        raise FileNotFoundError(f"client_secret khong tim thay: {secret_path}")
    flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
    # Port high khong ai dung de tranh bi app local (IIS/dev server) an redirect
    flow.redirect_uri = "http://localhost:8499"
    return flow


def main() -> int:
    parser = argparse.ArgumentParser(description="Manual OAuth consent (2 len)")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", action="store_true", help="Sinh auth URL")
    g.add_argument("--exchange", metavar="RESPONSE",
                   help="URL redirect hoac code de exchange")
    args = parser.parse_args()

    secret_env = os.environ.get("DUKICK_OAUTH_SECRET")
    token_env = os.environ.get("DUKICK_OAUTH_TOKEN")
    secret_path = Path(secret_env) if secret_env else DEFAULT_SECRET
    token_path = Path(token_env) if token_env else DEFAULT_TOKEN

    flow = make_flow(secret_path)
    pkce_file = BASE / ".pkce_verifier"

    if args.url:
        auth_url, _ = flow.authorization_url(
            access_type="offline", prompt="consent"
        )
        # Persist code_verifier (PKCE) cho len --exchange tiep theo
        if flow.code_verifier:
            pkce_file.write_text(flow.code_verifier, encoding="utf-8")
        print(auth_url)
        return 0

    # --exchange: load lai code_verifier da luu
    if pkce_file.exists():
        flow.code_verifier = pkce_file.read_text(encoding="utf-8").strip()

    try:
        resp = args.exchange.strip()
        if resp.startswith("http"):
            flow.fetch_token(authorization_response=resp)
        else:
            flow.fetch_token(code=resp)
    except Exception as exc:  # noqa: BLE001
        print(f"LOI exchange token: {exc}", file=sys.stderr)
        return 1

    creds = flow.credentials
    token_path.write_text(creds.to_json(), encoding="utf-8")
    # cleanup pkce verifier
    try:
        pkce_file.unlink()
    except OSError:
        pass
    print(f"OK. Token saved: {token_path}")
    print("Bay gio chay upload_to_drive.py binh thuong (khong can --auth).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
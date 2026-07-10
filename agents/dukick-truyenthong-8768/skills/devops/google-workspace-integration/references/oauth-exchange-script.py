#!/usr/bin/env python3
"""
OAuth2 authorization-code exchange for Google Workspace desktop app.

Usage:
    GAUTH_CODE="4/0A..." python references/oauth-exchange-script.py

Requirements:
    - client_secret_*.json file exists on disk (path hard-coded below or passed via env)
    - REDIRECT_URI in the script matches the one registered in Google Cloud Console
"""

import urllib.request
import urllib.parse
import json
import os
import sys

# ---------------------------------------------------------------------------
# CONFIG — adjust to your project
# ---------------------------------------------------------------------------
CREDENTIALS_PATH = r"C:\DuKickAgent\agents\dukick-truyenthong-8768\cache\documents\doc_52d046713e7d_client_secret_553888273742-03danr8q3i40uuhodfgiop73lvdmu28d.apps.googleusercontent.com.json"

REDIRECT_URI = "http://localhost:8499/"
SHARED_DIR = r"C:\DuKickAgent\agents\dukick-truyenthong-8768\shared"
OUTPUT_FILE = os.path.join(SHARED_DIR, "gauth_tokens.json")

# ---------------------------------------------------------------------------
# Read client credentials from JSON file (never embed in code)
# ---------------------------------------------------------------------------
with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
    creds = json.load(f)

CLIENT_ID = creds["installed"]["client_id"]
CLIENT_SECRET=creds[..._URI = os.environ.get("GAUTH_REDIRECT_URI", REDIRECT_URI)
CODE = os.environ.get("GAUTH_CODE", "")

if not CODE:
    print("ERROR: Set GAUTH_CODE environment variable before running.", file=sys.stderr)
    sys.exit(1)

os.makedirs(SHARED_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Exchange authorization code for tokens
# ---------------------------------------------------------------------------
post_data = urllib.parse.urlencode({
    "code": CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request(
    "https://oauth2.googleapis.com/token",
    data=post_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read().decode())

# ---------------------------------------------------------------------------
# Save tokens directly to file — NEVER print secrets
# ---------------------------------------------------------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Print only non-sensitive metadata
print(f"Tokens saved to: {OUTPUT_FILE}")
print(f"  access_token length : {len(result.get('access_token', ''))}")
print(f"  refresh_token length: {len(result.get('refresh_token', ''))}")
print(f"  expires_in          : {result.get('expires_in')}")
print(f"  scope               : {result.get('scope')}")

# ---------------------------------------------------------------------------
# Quick health-check: who is the authenticated user?
# ---------------------------------------------------------------------------
test_req = urllib.request.Request(
    "https://www.googleapis.com/drive/v3/about?fields=user",
    headers={"Authorization": f"Bearer {result['access_token']}"}
)
try:
    with urllib.request.urlopen(test_req, timeout=30) as test_resp:
        info = json.loads(test_resp.read().decode())
        user = info.get("user", {})
        print(f"\n✅ Connected as: {user.get('displayName')} <{user.get('emailAddress')}>")
except urllib.error.HTTPError as e:
    print(f"\n❌ Drive API test failed: {e.code} {e.reason}", file=sys.stderr)
    print(e.read().decode(), file=sys.stderr)
    sys.exit(1)

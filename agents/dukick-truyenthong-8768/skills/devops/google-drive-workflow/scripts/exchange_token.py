import urllib.request
import urllib.parse
import json
import os

"""
Exchange Google OAuth authorization_code for tokens.
Reads client_secret from shared/client_secret.json.
Saves tokens directly to shared/gauth_tokens.json — never prints to stdout.

Usage:
    GAUTH_CODE="4/0A..." python exchange_token.py
"""

SHARED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
CRED_PATH = os.path.join(SHARED_DIR, "client_secret.json")
REDIRECT_URI = "http://localhost:8499/"

def main():
    code = os.environ.get("GAUTH_CODE", "")
    if not code:
        print("ERROR: Set GAUTH_CODE env var")
        return 1

    with open(CRED_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)

    client_id = creds["installed"]["client_id"]
    client_secret = creds["installed"]["client_secret"]

    post_data = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=post_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())

    tokens_path = os.path.join(SHARED_DIR, "gauth_tokens.json")
    with open(tokens_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Tokens saved to", tokens_path)
    print("Access token length:", len(result.get("access_token", "")))
    print("Refresh token length:", len(result.get("refresh_token", "")))
    return 0

if __name__ == "__main__":
    exit(main())

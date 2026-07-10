import urllib.request
import urllib.parse
import json
import os
import sys

# Usage: set GAUTH_CODE env var, then run
#   GAUTH_CODE="4/0A..." python exchange_token.py

CRED_JSON = r"C:\DuKickAgent\agents\dukick-truyenthong-8768\cache\documents\doc_52d046713e7d_client_secret_553888273742-03danr8q3i40uuhodfgiop73lvdmu28d.apps.googleusercontent.com.json"
SHARED_DIR = r"C:\DuKickAgent\agents\dukick-truyenthong-8768\shared"
CODE = os.environ.get("GAUTH_CODE", "")

if not CODE:
    print("ERROR: Set GAUTH_CODE env var")
    sys.exit(1)

with open(CRED_JSON, "r", encoding="utf-8") as f:
    creds = json.load(f)["installed"]

post = urllib.parse.urlencode({
    "code": CODE,
    "client_id": creds["client_id"],
    "client_secret": creds["client_secret"],
    "redirect_uri": "http://localhost:8499/",
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request("https://oauth2.googleapis.com/token", data=post,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
with urllib.request.urlopen(req, timeout=30) as resp:
    tokens = json.loads(resp.read().decode())

os.makedirs(SHARED_DIR, exist_ok=True)
tokens_path = os.path.join(SHARED_DIR, "gauth_tokens.json")
with open(tokens_path, "w", encoding="utf-8") as f:
    json.dump(tokens, f, indent=2)

print(f"Tokens saved to: {tokens_path}")
print(f"access_token length: {len(tokens['access_token'])}")
print(f"refresh_token length: {len(tokens['refresh_token'])}")

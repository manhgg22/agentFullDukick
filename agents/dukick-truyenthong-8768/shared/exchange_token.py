import urllib.request
import urllib.parse
import json
import os

# Read client credentials from the uploaded file
cred_path = r"C:\DuKickAgent\agents\dukick-truyenthong-8768\cache\documents\doc_52d046713e7d_client_secret_553888273742-03danr8q3i40uuhodfgiop73lvdmu28d.apps.googleusercontent.com.json"
with open(cred_path, "r", encoding="utf-8") as f:
    creds = json.load(f)

CLIENT_ID = creds["installed"]["client_id"]
CLIENT_SECRET = creds["installed"]["client_secret"]
REDIRECT_URI = "http://localhost:8499/"
CODE = os.environ.get("GAUTH_CODE", "")

if not CODE:
    print("ERROR: Set GAUTH_CODE env var before running")
    exit(1)

SHARED_DIR = r"C:\DuKickAgent\agents\dukick-truyenthong-8768\shared"
os.makedirs(SHARED_DIR, exist_ok=True)

# Exchange code for tokens
post_data = urllib.parse.urlencode({
    "code": CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request("https://oauth2.googleapis.com/token", data=post_data, headers={"Content-Type": "application/x-www-form-urlencoded"})

with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read().decode())

# Save tokens directly to file (never printed)
tokens_path = os.path.join(SHARED_DIR, "gauth_tokens.json")
with open(tokens_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("Tokens saved to", tokens_path)
print("access_token length:", len(result.get("access_token", "")))
print("refresh_token length:", len(result.get("refresh_token", "")))
print("expires_in:", result.get("expires_in"))
print("token_type:", result.get("token_type"))
print("scope:", result.get("scope"))

# Test Drive API
print("\nTesting Drive API...")
test_req = urllib.request.Request(
    "https://www.googleapis.com/drive/v3/about?fields=user",
    headers={"Authorization": f"Bearer {result['access_token']}"}
)
try:
    with urllib.request.urlopen(test_req, timeout=30) as test_resp:
        test_result = json.loads(test_resp.read().decode())
        print("SUCCESS!")
        print(json.dumps(test_result, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print("FAILED:", e.code, e.reason)
    print(e.read().decode())

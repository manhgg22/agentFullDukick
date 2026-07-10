"""
shared/gauth.py — Google Auth Library cho Dukick agents
Cung cấp auto-refresh access_token từ Google OAuth 2.0.

Usage:
    from shared.gauth import get_access_token
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
"""

import json
import os
import time
import urllib.request
import urllib.parse

# Thư mục chứa file này (shared/)
SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SHARED_DIR, "gauth_tokens.json")

# Client credentials (đọc từ file JSON nếu có, fallback hardcoded)
CLIENT_ID = "553888273742-03danr8q3i40uuhodfgiop73lvdmu28d.apps.googleusercontent.com"
TOKEN_URI = "https://oauth2.googleapis.com/token"

def _load_creds():
    """Đọc client_secret từ file nếu tồn tại."""
    # Tìm file client_secret*.json trong shared
    for f in os.listdir(SHARED_DIR):
        if f.startswith("client_secret") and f.endswith(".json"):
            try:
                with open(os.path.join(SHARED_DIR, f), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                return data["installed"]["client_secret"]
            except Exception:
                pass
    # Fallback: đọc từ env
    return os.environ.get("GOOGLE_CLIENT_SECRET", "")

CLIENT_SECRET = _load_creds()

def _load_tokens():
    """Đọc tokens từ file JSON."""
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"Không tìm thấy {TOKEN_PATH}. Hãy chạy exchange_token.py trước.")
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_tokens(tokens):
    """Lưu tokens vào file JSON."""
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)

def _refresh_access_token(refresh_token):
    """Dùng refresh_token để lấy access_token mới."""
    if not CLIENT_SECRET:
        raise RuntimeError("CLIENT_SECRET chưa được cấu hình. Hãy copy file client_secret_*.json vào shared/")
    
    post_data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode()
    
    req = urllib.request.Request(TOKEN_URI, data=post_data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
    return result["access_token"], result.get("expires_in", 3599)

def get_access_token():
    """
    Trả về access_token hợp lệ (tự động refresh nếu đã hết hạn hoặc sắp hết hạn).
    
    Returns:
        str: access_token
    Raises:
        FileNotFoundError: nếu chưa có tokens
        RuntimeError: nếu refresh thất bại
    """
    tokens = _load_tokens()
    
    # Kiểm tra xem file đã bị modify bao lâu (dùng ctime/mtime vì không lưu timestamp)
    stat = os.stat(TOKEN_PATH)
    age_seconds = time.time() - stat.st_mtime
    
    # Nếu token cũ hơn 50 phút (expires_in = 3600s), refresh lại
    if age_seconds > 3000:  # 50 phút
        refresh_token = tokens.get("refresh_token")
        if not refresh_token:
            raise RuntimeError("Không có refresh_token. Cần re-auth.")
        
        new_access, expires_in = _refresh_access_token(refresh_token)
        tokens["access_token"] = new_access
        tokens["expires_in"] = expires_in
        _save_tokens(tokens)
        return new_access
    
    return tokens["access_token"]

def get_auth_header():
    """Trả về dict header Authorization đã sẵn sàng dùng."""
    return {"Authorization": f"Bearer {get_access_token()}"}

def test_connection():
    """Test kết nối Google Drive, trả về thông tin user."""
    req = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/about?fields=user",
        headers=get_auth_header()
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


if __name__ == "__main__":
    print("Testing Google Drive connection...")
    try:
        user_info = test_connection()
        user = user_info["user"]
        print(f"✅ Connected as: {user['displayName']} ({user['emailAddress']})")
    except Exception as e:
        print(f"❌ Failed: {e}")

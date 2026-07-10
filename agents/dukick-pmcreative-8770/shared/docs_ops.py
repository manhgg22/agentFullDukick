"""
shared/docs_ops.py — CRUD Google Docs (native) API.

Usage:
    from shared.docs_ops import create_doc, append_text, read_doc, insert_heading, replace_text
    doc = create_doc("Tiêu đề mới")
    append_text(doc['id'], "Đoạn văn bản mới.\n")
"""

import json
import urllib.request
from shared.gauth import get_auth_header

DOCS_URL = "https://docs.googleapis.com/v1/documents"

def create_doc(title):
    """Tạo Google Doc mới. Trả về {id, title, documentId}."""
    req = urllib.request.Request(
        DOCS_URL,
        data=json.dumps({"title": title}).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def read_doc(doc_id):
    """Đọc toàn bộ nội dung của một Google Doc."""
    req = urllib.request.Request(f"{DOCS_URL}/{doc_id}", headers=get_auth_header())
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def append_text(doc_id, text, end_of_doc=True):
    """
    Thêm text vào cuối (hoặc đầu) document.
    Trả về batchUpdate response.
    """
    # Lấy content length để xác định endIndex
    doc = read_doc(doc_id)
    body = doc.get("body", {})
    content = body.get("content", [])
    # Tìm endIndex cuối cùng
    end_index = 1
    for item in content:
        if "endIndex" in item:
            end_index = item["endIndex"]
    
    requests_payload = [{
        "insertText": {
            "location": {"index": end_index - 1 if end_of_doc else 1},
            "text": text
        }
    }]
    
    return _batch_update(doc_id, requests_payload)

def insert_heading(doc_id, text, heading_level=1):
    """Thêm heading vào cuối document."""
    doc = read_doc(doc_id)
    body = doc.get("body", {})
    content = body.get("content", [])
    end_index = 1
    for item in content:
        if "endIndex" in item:
            end_index = item["endIndex"]
    
    requests_payload = [
        {
            "insertText": {
                "location": {"index": end_index - 1},
                "text": f"{text}\n"
            }
        },
        {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": end_index - 1,
                    "endIndex": end_index - 1 + len(text) + 1
                },
                "paragraphStyle": {"namedStyleType": f"HEADING_{heading_level}"},
                "fields": "namedStyleType"
            }
        }
    ]
    return _batch_update(doc_id, requests_payload)

def replace_text(doc_id, old_text, new_text):
    """Thay thế toàn bộ old_text bằng new_text trong document."""
    requests_payload = [{
        "replaceAllText": {
            "containsText": {"text": old_text, "matchCase": True},
            "replaceText": new_text
        }
    }]
    return _batch_update(doc_id, requests_payload)

def _batch_update(doc_id, requests_list):
    """Internal: gọi docs.documents.batchUpdate."""
    req = urllib.request.Request(
        f"{DOCS_URL}/{doc_id}:batchUpdate",
        data=json.dumps({"requests": requests_list}).encode(),
        headers={**get_auth_header(), "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    print("Google Docs ops module loaded.")

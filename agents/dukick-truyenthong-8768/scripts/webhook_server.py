#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
import requests
from datetime import datetime
from flask import Flask, request, jsonify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("dukick-webhook")

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBHOOK_LOG = os.path.join(BASE_DIR, "debt_data", "webhook_logs.jsonl")
ZALO_CONFIG_PATH = os.path.join(BASE_DIR, "debt_data", "zalo_config.json")

os.makedirs(os.path.dirname(WEBHOOK_LOG), exist_ok=True)

# Load env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

def load_zalo_config():
    try:
        with open(ZALO_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Cannot load zalo_config.json: {e}")
        return {}

ZALO_CFG = load_zalo_config()
BOT_TOKEN = ZALO_CFG.get("bot_token", "")
SECRET_TOKEN = ZALO_CFG.get("secret_token", "")
ZALO_API_URL = "https://bot-api.zaloplatforms.com/bot{}/sendMessage"

def log_payload(source, payload):
    entry = {
        "received_at": datetime.now().isoformat(),
        "source": source,
        "payload": payload
    }
    with open(WEBHOOK_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    logger.info(f"[{source}] logged payload")

def send_zalo_message(chat_id, text):
    if not BOT_TOKEN or len(BOT_TOKEN) < 50:
        logger.warning("BOT_TOKEN chưa được cấu hình đúng")
        return False
    url = ZALO_API_URL.format(BOT_TOKEN)
    payload = {"chat_id": chat_id, "text": text}
    try:
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()
        logger.info(f"Zalo API response: {data}")
        return data.get("ok") == True
    except Exception as e:
        logger.error(f"Failed to send Zalo message: {e}")
        return False

def get_debt_context():
    debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
    try:
        with open(debt_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        debts = db.get("debts", [])
        if not debts:
            return "Hiện không có công nợ nào."
        total = sum(d["amount"] for d in debts if d["status"] in ("pending","overdue"))
        overdue = [d for d in debts if d["status"] == "overdue"]
        lines = [f"Tổng công nợ đang chờ thu: {total:,.0f} VND"]
        if overdue:
            lines.append(f"Quá hạn ({len(overdue)} khoản):")
            for d in overdue:
                lines.append(f"- {d['client_name']} ({d['project']}): {d['amount']:,.0f} VND, hạn {d['due_date']}")
        pending = [d for d in debts if d["status"] == "pending"]
        if pending:
            lines.append(f"\nChờ thanh toán ({len(pending)} khoản):")
            for d in pending:
                lines.append(f"- {d['client_name']} ({d['project']}): {d['amount']:,.0f} VND, hạn {d['due_date']}")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi đọc công nợ: {e}"

def call_ai(user_text, chat_id):
    if not OPENAI_API_KEY:
        return "🤖 Bot Dukick: AI chưa được cấu hình. Nhắn 'help'."
    
    debt_ctx = get_debt_context()
    
    system_prompt = """Bạn là Agent #7 — Đòi Công Nợ của Dukick. Bạn trả lời thông minh, ngắn gọn, tự nhiên bằng tiếng Việt.

THÔNG TIN CÔNG NỢ HIỆN TẠI:
""" + debt_ctx + """

HƯỚNG DẪN:
- Trả lời thân thiện, như nhân viên tư vấn
- Nếu user hỏi về công nợ, đưa thông tin cụ thể từ context trên
- Nếu user nhắn chào hỏi, chào lại và gợi ý xem công nợ
- Nếu user hỏi không liên quan, trả lời lịch sự và gợi ý help
- Tên công ty là Dukick, bạn là bot của Dukick
- Ký hiệu tiền: VND (dùng dấu chấm phân cách nghìn)"""
    
    try:
        url = f"{OPENAI_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return "🤖 Bot Dukick: Đang gặp sự cố, bạn thử lại sau!"
    except Exception as e:
        return f"🤖 Bot Dukick: Lỗi AI. Nhắn 'help'."

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Dukick Webhook Server (Zalo Bot + AI)",
        "status": "running",
        "time": datetime.now().isoformat(),
        "port": 8888
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/webhook/zalo", methods=["POST", "GET"])
def webhook_zalo():
    if request.method == "POST":
        try:
            data = request.get_json(force=True, silent=True) or {}
        except Exception:
            data = {"raw": request.data.decode("utf-8", errors="replace")}
    else:
        data = dict(request.args)

    secret_header = request.headers.get("X-Bot-Api-Secret-Token", "")
    if SECRET_TOKEN and secret_header != SECRET_TOKEN:
        return jsonify({"status": "unauthorized"}), 403

    log_payload("zalo", data)

    result = data.get("result", data)
    event_name = result.get("event_name", "")
    logger.info(f"Zalo event: {event_name}")

    if event_name == "message.text.received":
        msg = result.get("message", {})
        text = msg.get("text", "")
        chat_info = msg.get("chat", {})
        chat_id = chat_info.get("id")
        sender_info = msg.get("from", {})
        user_id = sender_info.get("id")

        logger.info(f"Bot msg from {user_id} in chat {chat_id}: {text}")

        if text and chat_id:
            reply = call_ai(text, chat_id)
            send_zalo_message(chat_id, reply)

    return jsonify({"status": "received"}), 200

@app.route("/webhook/<source>", methods=["POST", "GET"])
def webhook_generic(source):
    if request.method == "POST":
        try:
            data = request.get_json(force=True, silent=True) or request.form.to_dict()
        except Exception:
            data = {"raw": request.data.decode("utf-8", errors="replace")}
    else:
        data = dict(request.args)

    log_payload(source, data)
    return jsonify({"status": "received", "source": source}), 200

@app.route("/webhook/debt/update", methods=["POST"])
def debt_update():
    data = request.get_json(force=True, silent=True) or {}
    log_payload("debt-update", data)

    debt_id = data.get("id")
    new_status = data.get("status")
    if not debt_id or not new_status:
        return jsonify({"error": "Missing 'id' or 'status'"}), 400

    debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
    try:
        with open(debt_path, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Cannot load debts.json: {e}"}), 500

    updated = False
    for debt in db.get("debts", []):
        if debt["id"] == debt_id:
            debt["status"] = new_status
            debt.setdefault("notes", "")
            if data.get("notes"):
                debt["notes"] += f" | {data['notes']}"
            debt["last_reminder"] = datetime.now().isoformat()
            updated = True
            break

    if not updated:
        return jsonify({"error": f"Debt {debt_id} not found"}), 404

    with open(debt_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    logger.info(f"Debt {debt_id} updated to '{new_status}'")
    return jsonify({"status": "updated", "id": debt_id, "new_status": new_status}), 200

if __name__ == "__main__":
    logger.info("Starting Dukick Webhook Server (Zalo Bot + AI) on port 8888")
    app.run(host="0.0.0.0", port=8888, debug=False)

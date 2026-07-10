#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dukick agentThuno — Zalo Bot đòi nợ / thu nợ công nợ.
Webhook server nhận payload Zalo Bot Platform → gọi ollama (kimi-k2.6) → reply Zalo.
Port 8889 (truyenthong dùng 8888)."""
import os
import sys
import json
import logging
import requests
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify

# Load .env tu thu muc agent (agents/dukick-thuno-8773/)
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(_env_file)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("dukick-thuno-webhook")

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBHOOK_LOG = os.path.join(BASE_DIR, "debt_data", "webhook_logs.jsonl")
ZALO_CONFIG_PATH = os.path.join(BASE_DIR, "debt_data", "zalo_config.json")
PORT = 8889

os.makedirs(os.path.dirname(WEBHOOK_LOG), exist_ok=True)

# Load env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://ollama.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "glm-5.2")  # non-reasoning: content ra ngay, k lo empty nhu kimi-k2.6

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
        logger.warning("BOT_TOKEN chưa được cấu hình đúng (cần >= 50 ký tự)")
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

def get_debt_context(client_filter: str = "") -> str:
    """Tra ve context lich thanh toan.
    Neu co client_filter → chi lay khoan cua client do.
    Neu khong → chi tra ve tong hop (khong list tung dong).
    """
    debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
    try:
        with open(debt_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        debts = db.get("debts", [])
        if not debts:
            return "Chua co lich thanh toan nao trong he thong."

        if client_filter:
            kw = client_filter.lower()
            debts = [d for d in debts if kw in d.get("client_name", "").lower()
                     or kw in d.get("project", "").lower()]
            if not debts:
                return f"Khong tim thay khoan nao lien quan den '{client_filter}'."
            lines = [f"Lich thanh toan lien quan den '{client_filter}':"]
            for d in debts:
                tag = "chua nhan xac nhan" if d["status"] == "overdue" else ("sap den lich" if d["status"] == "pending" else "da thanh toan")
                lines.append(f"- {d['project']}: {d['amount']:,.0f} VND | du kien {d['due_date']} | {tag}")
            return "\n".join(lines)

        # Chi tra tong hop, KHONG list tung khoan
        late = [d for d in debts if d["status"] == "overdue"]
        pending = [d for d in debts if d["status"] == "pending"]
        total_late = sum(d["amount"] for d in late)
        total_pending = sum(d["amount"] for d in pending)
        return (
            f"Tong hop lich thanh toan:\n"
            f"- Chua nhan xac nhan (da qua ngay du kien): {len(late)} khoan, tong {total_late:,.0f} VND\n"
            f"- Sap den lich: {len(pending)} khoan, tong {total_pending:,.0f} VND\n"
            f"Neu anh/chi muon biet cu the khoan nao, vui long cho biet ten project hoac khach hang."
        )
    except Exception as e:
        return f"Loi doc lich thanh toan: {e}"

def lookup_by_zalo_id(zalo_id: str) -> str:
    """Tìm khách hàng theo Zalo ID (contact_phone), trả về thông tin công nợ."""
    debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
    try:
        with open(debt_path, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception as e:
        return f"Loi doc debts.json: {e}"

    matched = [d for d in db.get("debts", []) if d.get("contact_phone", "").strip() == zalo_id.strip()]
    if not matched:
        return (
            f"Khong tim thay ai voi Zalo ID: {zalo_id}\n"
            f"(ID chua duoc gan vao debts.json, them vao field 'contact_phone')"
        )

    client_name = matched[0].get("client_name", "?")
    lines = [f"Zalo ID {zalo_id} → {client_name}"]
    total = sum(d["amount"] for d in matched if d["status"] != "paid")
    lines.append(f"Tong no chua thanh toan: {total:,.0f} VND ({len(matched)} khoan)")
    for d in matched:
        status_label = {"overdue": "QUA HAN", "pending": "Cho TT", "paid": "Da tra"}.get(d["status"], d["status"])
        lines.append(
            f"  [{status_label}] {d['project'][:50]} | {d['amount']:,.0f} VND | han: {d['due_date'] or 'chua ro'}"
        )
    return "\n".join(lines)


def save_contact(zalo_id: str, debt_ids: list[str] | None = None) -> str:
    """Gan Zalo ID vao tat ca khoan no cua client (theo debt_id hoac tu dong theo client_name)."""
    # Dung cho admin: /setid <zalo_id> <debt_id1,debt_id2,...>
    debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
    try:
        with open(debt_path, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception as e:
        return f"Loi: {e}"

    updated = 0
    for debt in db.get("debts", []):
        if debt_ids is None or debt["id"] in debt_ids:
            debt["contact_phone"] = zalo_id
            updated += 1

    with open(debt_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return f"Da cap nhat {updated} khoan voi Zalo ID {zalo_id}"


def handle_command(text: str, sender_id: str | None) -> str | None:
    """Xu ly lenh admin. Tra None neu khong phai lenh → fallback sang AI."""
    text = text.strip()

    # /help  →  danh sach cau lenh
    if text.lower() in ("/help", "help", "cac lenh", "câu lệnh", "lenh"):
        return (
            "Cac cau lenh:\n"
            "/help — xem danh sach lenh\n"
            "/list overdue — khoan chua nhan xac nhan\n"
            "/list pending — khoan sap den lich\n"
            "/list all — toan bo 75 khoan\n"
            "/debts <ten> — tim theo ten khach (vd: /debts The One)\n"
            "/paid <DEBT-ID> [ghi chu] — danh dau da thanh toan + sync Google Sheet\n"
            "/check — xem khoan cua chinh minh\n"
            "/check <zalo_id> — xem khoan cua nguoi khac\n"
            "/setid <zalo_id> <DEBT-0001,DEBT-0002> — gan Zalo ID vao khoan\n"
            "\nHoac chat binh thuong, em tra loi AI."
        )

    # /check <zalo_id>  →  tra cuu khach theo ID
    if text.lower().startswith("/check "):
        zalo_id = text[7:].strip()
        return lookup_by_zalo_id(zalo_id)

    # /check  (khong co ID) → tra cuu chinh nguoi gui
    if text.lower() == "/check" and sender_id:
        return lookup_by_zalo_id(sender_id)

    # /setid <zalo_id> <DEBT-0001,DEBT-0002>  →  gan ID vao cac khoan no
    if text.lower().startswith("/setid "):
        parts = text[7:].strip().split()
        if len(parts) < 2:
            return "Cu phap: /setid <zalo_id> <DEBT-0001,DEBT-0002,...>"
        zalo_id = parts[0]
        debt_ids = [x.strip() for x in parts[1].split(",")]
        return save_contact(zalo_id, debt_ids)

    # /list overdue | pending | all  →  liet ke, gui nhieu tin neu > 20
    if text.lower().startswith("/list"):
        filter_status = text[5:].strip().lower() or "all"
        debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
        try:
            with open(debt_path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception as e:
            return f"Loi: {e}"
        debts = db.get("debts", [])
        if filter_status != "all":
            debts = [d for d in debts if d["status"] == filter_status]
        if not debts:
            return f"Khong co khoan nao ({filter_status})"
        # Chia thanh cac chunk 20 dong, gui lan luot
        chunk_size = 20
        chunks = [debts[i:i+chunk_size] for i in range(0, len(debts), chunk_size)]
        messages = []
        for ci, chunk in enumerate(chunks):
            header = f"=== {filter_status.upper()} ({len(debts)} khoan) — phan {ci+1}/{len(chunks)} ==="
            lines = [header]
            for d in chunk:
                amt = f"{d['amount']:,.0f}" if d['amount'] else "?"
                lines.append(f"{d['id']} | {d['client_name'][:22]} | {amt} | {d['due_date'] or 'chua ro'}")
            messages.append("\n".join(lines))
        # Tra tin dau tien, gui phan con lai qua send_zalo_message
        # (sender_id khong co trong scope nay, dung chat_id qua closure)
        return "\n__MULTI__\n".join(messages)

    # /paid <DEBT-ID> [ghi chu]  →  danh dau da thanh toan, update Sheet
    if text.lower().startswith("/paid "):
        parts = text[6:].strip().split(None, 1)
        if not parts:
            return "Cu phap: /paid <DEBT-ID> [ghi chu] (vd: /paid DEBT-0005 da chuyen 03/07)"
        debt_id = parts[0].upper()
        notes = parts[1] if len(parts) > 1 else ""
        # Update local
        debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
        try:
            with open(debt_path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception as e:
            return f"Loi doc file: {e}"
        debt = next((d for d in db.get("debts", []) if d["id"] == debt_id), None)
        if not debt:
            return f"Khong tim thay {debt_id}"
        old_status = debt["status"]
        debt["status"] = "paid"
        if notes:
            debt["notes"] = (debt.get("notes") or "") + f" | {notes}"
        debt["last_reminder"] = datetime.now().strftime("%Y-%m-%d")
        with open(debt_path, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        # Sync len Google Sheet (background)
        try:
            import subprocess
            sync_script = os.path.join(BASE_DIR, "scripts", "sync_sheets.py")
            subprocess.Popen(
                [sys.executable, sync_script, "update", debt_id, "paid", notes or "Da thanh toan"],
                cwd=BASE_DIR
            )
            sheet_note = " + dang sync Google Sheet"
        except Exception:
            sheet_note = " (Sheet sync that bai, check log)"
        return (
            f"[OK] {debt_id} cap nhat: {old_status} -> paid\n"
            f"Project: {debt['project'][:50]}\n"
            f"So tien: {debt['amount']:,.0f} VND\n"
            f"{notes and f'Ghi chu: {notes}' or ''}{sheet_note}"
        )

    # /debts <ten khach>  ->  tim tat ca khoan cua khach do
    if text.lower().startswith("/debts"):
        keyword = text[6:].strip()
        if not keyword:
            return "Cu phap: /debts <ten khach> (vd: /debts The One)"
        debt_path = os.path.join(BASE_DIR, "debt_data", "debts.json")
        try:
            with open(debt_path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception as e:
            return f"Loi: {e}"
        kw = keyword.lower()
        matched = [d for d in db.get("debts", [])
                   if kw in d.get("client_name", "").lower() or kw in d.get("project", "").lower()]
        if not matched:
            return f"Khong tim thay khoan nao chua '{keyword}'"
        total = sum(d["amount"] for d in matched if d["status"] != "paid")
        lines = [f"=== '{keyword}' ({len(matched)} khoan, tong: {total:,.0f} VND) ==="]
        for d in matched:
            tag = {"overdue": "QUA HAN", "pending": "Cho TT", "paid": "Da TT"}.get(d["status"], d["status"])
            contact = d.get("contact_phone", "") or "chua gan ID"
            lines.append(f"{d['id']} [{tag}] {d['project'][:35]} | {d['amount']:,.0f} | han:{d['due_date'] or '?'} | zalo:{contact}")
        return "\n".join(lines)

    return None


def call_ai(user_text, chat_id):
    if not OPENAI_API_KEY:
        return "agentThuno: AI chua cau hinh (OPENAI_API_KEY trong). Nhan 'help'."

    # Chi inject debt context khi user hoi ve thanh toan/project cu the
    PAYMENT_KW = ("thanh toan", "hop dong", "project", "khoan", "tien", "chuyen", "bao nhieu",
                  "khi nao", "han", "nomad", "vng", "hns", "may10", "sun", "global", "the one")
    need_ctx = any(kw in user_text.lower() for kw in PAYMENT_KW)
    debt_ctx = get_debt_context(client_filter=user_text) if need_ctx else ""

    ctx_section = f"\n\nDỮ LIỆU LỊCH THANH TOÁN:\n{debt_ctx}" if debt_ctx else ""

    system_prompt = (
        "Bạn là Dukick Agent Service — trợ lý AI của Dukick trên Zalo.\n"
        "Trả lời bằng tiếng Việt, thân thiện, tự nhiên. Xưng 'em', gọi 'anh/chị'.\n"
        "Bạn có thể trả lời câu hỏi chung, hỗ trợ tra cứu lịch thanh toán theo hợp đồng, "
        "và nhắc lịch chuyển khoản.\n"
        "KHÔNG dùng từ 'đòi nợ', 'nợ xấu', 'quá hạn' — dùng 'lịch thanh toán', 'dự kiến chuyển khoản'.\n"
        "KHÔNG tự liệt kê danh sách khi không được hỏi.\n"
        "KHÔNG tự điều chỉnh số tiền hoặc cam kết gia hạn."
        + ctx_section
    )

    try:
        url = f"{OPENAI_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": AI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            msg = data["choices"][0]["message"]
            content = msg.get("content") or ""
            if not content.strip():
                # Reasoning model tra ve thinking nhung content rong
                # → lay noi dung tu reasoning field lam fallback
                reasoning = msg.get("reasoning") or msg.get("reasoning_content") or ""
                if reasoning.strip():
                    # Cat lay phan sau cung cua reasoning (phan ket luan)
                    lines = [l.strip() for l in reasoning.strip().splitlines() if l.strip()]
                    # Lay toi da 5 dong cuoi (phan ket luan)
                    answer = "\n".join(lines[-5:]) if len(lines) > 5 else "\n".join(lines)
                    return answer
                return "Xin loi anh/chi, em chua xu ly duoc yeu cau nay. Anh/chi vui long thu lai."
            return content
        logger.warning(f"Unexpected API response: {data}")
        return "Xin loi anh/chi, he thong dang co su co. Vui long thu lai sau."
    except Exception as e:
        logger.error(f"AI call failed: {e}")
        return "🤖 agentThuno: Lỗi AI. Nhắn 'help'."

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Dukick agentThuno — Zalo Bot đòi nợ (AI: ollama kimi-k2.6)",
        "status": "running",
        "time": datetime.now().isoformat(),
        "port": PORT
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
            import re as _re
            clean_text = _re.sub(r"^@\S+\s*", "", text).strip()

            def process_and_reply(txt, cid, uid):
                try:
                    reply = handle_command(txt, uid) or call_ai(txt, cid)
                    # Neu co nhieu phan (tu /list), gui tung tin
                    parts = reply.split("\n__MULTI__\n")
                    for part in parts:
                        send_zalo_message(cid, part)
                except Exception as exc:
                    logger.error(f"process_and_reply error: {exc}")

            threading.Thread(target=process_and_reply, args=(clean_text, chat_id, user_id), daemon=True).start()

    # Tra 200 NGAY cho Zalo truoc khi xu ly AI (tranh timeout/retry)
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
    logger.info(f"Starting agentThuno webhook server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
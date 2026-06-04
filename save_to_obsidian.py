"""
Hook script: pre_gateway_dispatch
Tự động lưu mọi tin nhắn Discord vào Obsidian vault theo ngày.
"""
import json, sys, os, re
from datetime import datetime
from pathlib import Path

VAULT_ROOT = r"C:\Users\Admin\Documents\Obsidian Vault"

# Map agent → vault mặc định (khi không xác định được server)
AGENT_VAULT_MAP = {
    "dukick-tong-8767":        "DuKick-Tong",
    "dukick-truyenthong-8768": "DuKick-TruyenThong",
    "dukick-pm-8769":          "DuKick-PM",
    "dukick-pmcreative-8770":  "DuKick-PMCreative",
    "dukick-ketoan-8771":      "DuKick-NeoLab",
}

# Map guild_id → vault folder
GUILD_VAULT_MAP = {
    "1092673756457074760": "DuKick-PM",           # 🔥 DUKICK
    "1489834585176015018": "Hanoi-Signature",      # Hanoi Signature
    "1512008093834285146": "Photoshoot-HNS",       # Photoshoot HNS
}

def get_vault_folder(guild_id: str = None) -> Path | None:
    # Ưu tiên theo server
    if guild_id and guild_id in GUILD_VAULT_MAP:
        vault_name = GUILD_VAULT_MAP[guild_id]
    else:
        # Fallback theo agent
        hermes_home = os.environ.get("HERMES_HOME", "")
        vault_name = None
        for key, vname in AGENT_VAULT_MAP.items():
            if key in hermes_home:
                vault_name = vname
                break
    if not vault_name:
        return None
    folder = Path(VAULT_ROOT) / vault_name / "Discord"
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def extract_message(payload: dict) -> dict | None:
    extra = payload.get("extra", {})
    event = extra.get("event", {})
    if not event:
        return None

    # Hỗ trợ cả dict và object string
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except Exception:
            return None

    text = event.get("text") or event.get("content") or ""
    sender = (
        event.get("sender_name")
        or event.get("author", {}).get("display_name")
        or event.get("author", {}).get("username")
        or event.get("user_name")
        or "Unknown"
    )
    platform = event.get("platform") or payload.get("extra", {}).get("platform", "discord")
    attachments = event.get("attachments") or []

    return {
        "text": text.strip(),
        "sender": sender,
        "platform": platform,
        "attachments": attachments,
    }

def format_entry(msg: dict, now: datetime) -> str:
    time_str = now.strftime("%H:%M")
    lines = [f"\n### {time_str} — {msg['sender']}"]

    if msg["text"]:
        lines.append(msg["text"])

    for att in msg["attachments"]:
        name = att.get("filename") or att.get("name") or "file"
        url  = att.get("url") or att.get("proxy_url") or ""
        if url:
            lines.append(f"📎 [{name}]({url})")
        else:
            lines.append(f"📎 {name}")

    return "\n".join(lines)

def append_to_daily_note(folder: Path, entry: str, now: datetime) -> None:
    date_str  = now.strftime("%Y-%m-%d")
    note_path = folder / f"{date_str}.md"

    if not note_path.exists():
        header = f"# Discord Log — {date_str}\n"
        note_path.write_text(header, encoding="utf-8")

    with note_path.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    # Chỉ xử lý pre_gateway_dispatch
    if payload.get("hook_event_name") != "pre_gateway_dispatch":
        sys.exit(0)

    # Lấy guild_id từ event để xác định server
    extra = payload.get("extra", {})
    event = extra.get("event", {})
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except Exception:
            event = {}
    guild_id = str(event.get("guild_id") or "")

    vault_folder = get_vault_folder(guild_id)
    if not vault_folder:
        sys.exit(0)

    msg = extract_message(payload)
    if not msg or (not msg["text"] and not msg["attachments"]):
        sys.exit(0)

    now = datetime.now()
    entry = format_entry(msg, now)
    append_to_daily_note(vault_folder, entry, now)

    # Trả về allow để không chặn message
    print(json.dumps({"action": "allow"}))

if __name__ == "__main__":
    main()

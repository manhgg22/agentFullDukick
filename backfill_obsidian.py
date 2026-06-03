"""
Backfill: Kéo toàn bộ lịch sử tin nhắn Discord về Obsidian vault.
Chạy: python backfill_obsidian.py
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

# ─── Config ───────────────────────────────────────────────────────────────────

AGENTS = [
    {
        "name": "dukick-truyenthong-8768",
        "env": r"C:\DuKickAgent\dukick-truyenthong-8768\.env",
        "vault": r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-TruyenThong",
    },
    {
        "name": "dukick-tong-8767",
        "env": r"C:\DuKickAgent\dukick-tong-8767\.env",
        "vault": r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-Tong",
    },
    {
        "name": "dukick-pm-8769",
        "env": r"C:\DuKickAgent\dukick-pm-8769\.env",
        "vault": r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-PM",
    },
    {
        "name": "dukick-pmcreative-8770",
        "env": r"C:\DuKickAgent\dukick-pmcreative-8770\.env",
        "vault": r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-PMCreative",
    },
    {
        "name": "dukick-ketoan-8771",
        "env": r"C:\DuKickAgent\dukick-ketoan-8771\.env",
        "vault": r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-NeoLab",
    },
]


def load_env(env_path):
    env = {}
    try:
        for line in Path(env_path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    except Exception:
        pass
    return env


def discord_get(endpoint, token, params=None):
    url = f"https://discord.com/api/v10{endpoint}"
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (https://discord.com, 10)",
        "Content-Type": "application/json",
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"  HTTP {r.status_code}: {r.text[:100]}")
            return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def fetch_all_messages(channel_id, token):
    """Kéo toàn bộ tin nhắn từ channel, trả về list sorted cũ → mới."""
    all_msgs = []
    before = None
    page = 0
    while True:
        params = {"limit": "100"}
        if before:
            params["before"] = before
        msgs = discord_get(f"/channels/{channel_id}/messages", token, params)
        if not msgs:
            break
        all_msgs.extend(msgs)
        page += 1
        print(f"  Fetched page {page}: {len(msgs)} messages (total: {len(all_msgs)})")
        if len(msgs) < 100:
            break
        before = msgs[-1]["id"]
        time.sleep(0.5)  # Tránh rate limit

    all_msgs.reverse()  # Sắp xếp cũ → mới
    return all_msgs


def snowflake_to_dt(snowflake_id):
    """Convert Discord snowflake ID to datetime."""
    ts = (int(snowflake_id) >> 22) + 1420070400000
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc)


def save_messages_to_vault(messages, vault_path, channel_name):
    """Ghi tin nhắn vào daily notes trong Obsidian vault."""
    vault = Path(vault_path) / "Discord"
    vault.mkdir(parents=True, exist_ok=True)

    # Nhóm theo ngày
    by_date = {}
    for msg in messages:
        if msg.get("type", 0) not in (0, 19):  # Chỉ lấy tin nhắn thường và replies
            continue
        content = msg.get("content", "").strip()
        attachments = msg.get("attachments", [])
        if not content and not attachments:
            continue

        dt = snowflake_to_dt(msg["id"])
        local_dt = dt.astimezone()
        date_str = local_dt.strftime("%Y-%m-%d")
        time_str = local_dt.strftime("%H:%M")
        author = msg.get("author", {})
        sender = author.get("global_name") or author.get("username") or "Unknown"

        entry_lines = [f"\n### {time_str} — {sender}"]
        if content:
            entry_lines.append(content)
        for att in attachments:
            name = att.get("filename", "file")
            url = att.get("url", "")
            if url:
                entry_lines.append(f"📎 [{name}]({url})")
            else:
                entry_lines.append(f"📎 {name}")

        by_date.setdefault(date_str, []).append("\n".join(entry_lines))

    # Ghi vào từng daily note
    saved = 0
    for date_str, entries in sorted(by_date.items()):
        note_path = vault / f"{date_str}.md"
        header = f"# Discord Log — {date_str} (#{channel_name})\n"

        # Nếu file đã tồn tại, không ghi đè — append nếu chưa có entry
        if note_path.exists():
            existing = note_path.read_text(encoding="utf-8")
            new_entries = []
            for entry in entries:
                # Lấy timestamp từ entry để kiểm tra trùng
                first_line = entry.strip().splitlines()[0] if entry.strip() else ""
                if first_line not in existing:
                    new_entries.append(entry)
            if new_entries:
                with note_path.open("a", encoding="utf-8") as f:
                    f.write("\n".join(new_entries) + "\n")
                saved += len(new_entries)
        else:
            with note_path.open("w", encoding="utf-8") as f:
                f.write(header + "\n".join(entries) + "\n")
            saved += len(entries)

    return saved, len(by_date)


def main():
    print("=" * 60)
    print("DuKick Discord → Obsidian Backfill")
    print("=" * 60)

    total_saved = 0

    for agent in AGENTS:
        print(f"\n[{agent['name']}]")
        env = load_env(agent["env"])
        token = env.get("DISCORD_BOT_TOKEN", "")
        channel_id = env.get("DISCORD_HOME_CHANNEL", "")

        if not token:
            print("  ⚠️  No DISCORD_BOT_TOKEN — skip")
            continue
        if not channel_id:
            print("  ⚠️  No DISCORD_HOME_CHANNEL — skip")
            continue

        # Lấy tên channel
        ch_info = discord_get(f"/channels/{channel_id}", token)
        channel_name = ch_info.get("name", channel_id) if ch_info else channel_id
        print(f"  Channel: #{channel_name} ({channel_id})")

        # Kéo tin nhắn
        print(f"  Fetching messages...")
        messages = fetch_all_messages(channel_id, token)
        print(f"  Total messages: {len(messages)}")

        if not messages:
            print("  ⚠️  No messages found")
            continue

        # Lưu vào Obsidian
        saved, days = save_messages_to_vault(messages, agent["vault"], channel_name)
        total_saved += saved
        print(f"  ✅ Saved {saved} entries across {days} days → {agent['vault']}\\Discord\\")

    print(f"\n{'=' * 60}")
    print(f"Done! Total {total_saved} entries saved to Obsidian.")


if __name__ == "__main__":
    main()

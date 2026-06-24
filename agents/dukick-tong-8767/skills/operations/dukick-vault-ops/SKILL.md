---
name: Dukick-vault-ops
description: >
  Reliable access to Dukick's 5 Obsidian vaults on the Windows host.
  Covers directory layout, Discord log file conventions, and the critical
  Windows-path workaround (use execute_code + Python instead of read_file/terminal).
triggers:
  - Need to read vault files from Dukick-Tong, Dukick-PM, Dukick-TruyenThong, Dukick-PMCreative, or Dukick-NeoLab
  - read_file or terminal fails on vault paths
  - Need to list, search, or parse Discord logs or Báo cáo files
---

# Dukick Vault Operations

## Vault Layout

All 5 vaults live under the same parent directory:

```
C:\Users\Admin\Documents\Obsidian Vault\
├── Dukick-Tong\          (CEO Assistant)
│   ├── Báo cáo\
│   ├── Discord\
│   └── README.md
├── Dukick-PM\            (Account)
│   ├── Discord\
│   ├── TaiLieu-Account\
│   └── README.md
├── Dukick-TruyenThong\   (Sales)
│   ├── Discord\
│   ├── TaiLieu-Sales\
│   └── README.md
├── Dukick-PMCreative\    (Creative)
│   ├── Discord\
│   ├── TaiLieu-Creative\
│   └── README.md
└── Dukick-NeoLab\        (Finance)
    ├── Discord\
    ├── TaiLieu-Finance\
    └── README.md
```

> **Path constant**: Store the vault root in a variable so it never drifts:
> `VAULT_ROOT = r"C:\Users\Admin\Documents\Obsidian Vault"`

## Discord Log Files

Each vault's `Discord\` folder contains daily log files named `YYYY-MM-DD.md`.

- One file per calendar day.
- If a date file is **missing**, no Discord activity was logged for that day in that bộ phận.
- Files are UTF-8 but may carry a **BOM** (`\ufeff`). Use `encoding="utf-8-sig"` when opening.

### Listing / searching logs (Python pattern)

```python
import os, glob

vault = r"C:\Users\Admin\Documents\Obsidian Vault\Dukick-PM"
discord_dir = os.path.join(vault, "Discord")
files = sorted(os.listdir(discord_dir))   # already sorted by date string
latest = files[-1] if files else None
```

## ⚠️ CRITICAL: Windows Path Workaround

On this Windows host both `read_file` and `terminal` are **unreliable** for vault paths:

| Tool | Failure mode |
|------|-------------|
| `read_file` | "File not found" on **any** path under the `Obsidian Vault` tree — even simple filenames like `2026-06-04.md`. The failure is systematic, not limited to spaces or Vietnamese characters. |
| `terminal` | WSL not installed → every shell command errors out |

**Always use `execute_code` with Python** for vault file I/O.

### Read a vault file

```python
import os

path = r"C:\Users\Admin\Documents\Obsidian Vault\Dukick-Tong\Báo cáo\2026-06-03_Báo-cáo-tổng-hợp.md"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()
print(content[:2000])
```

### List a directory

```python
import os

dir_path = r"C:\Users\Admin\Documents\Obsidian Vault\Dukick-PM\TaiLieu-Account"
files = os.listdir(dir_path)
print(files)
```

### Check existence before read

```python
import os

path = os.path.join(vault, "Discord", "2026-06-04.md")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        print(f.read())
else:
    print("No log for this date.")
```

### Batch-read multiple vaults

```python
import os

VAULT_ROOT = r"C:\Users\Admin\Documents\Obsidian Vault"
vaults = {
    "Tong": "Dukick-Tong",
    "PM": "Dukick-PM",
    "TruyenThong": "Dukick-TruyenThong",
    "PMCreative": "Dukick-PMCreative",
    "NeoLab": "Dukick-NeoLab",
}

def read_latest_discord(vault_name):
    discord_dir = os.path.join(VAULT_ROOT, vaults[vault_name], "Discord")
    if not os.path.isdir(discord_dir):
        return None
    files = sorted(os.listdir(discord_dir))
    if not files:
        return None
    latest = os.path.join(discord_dir, files[-1])
    with open(latest, "r", encoding="utf-8-sig") as f:
        return f.read()
```

## TaiLieu / Báo cáo Subfolders

| Vault | Subfolder | Purpose |
|-------|-----------|---------|
| Dukick-Tong | `Báo cáo` | Báo cáo tổng hợp định kỳ (agent-generated) |
| Dukick-PM | `TaiLieu-Account` | SOP, case study, tài liệu nghiệp vụ Account |
| Dukick-TruyenThong | `TaiLieu-Sales` | Elevator pitch, email mẫu, list câu hỏi sale |
| Dukick-PMCreative | `TaiLieu-Creative` | Quy trình creative, treatment |
| Dukick-NeoLab | `TaiLieu-Finance` | Hợp đồng mẫu, quy trình chứng từ, tạm ứng |

## Search Strategy

When hunting for a specific deliverable (kịch bản, treatment, script, brief), follow this order to avoid broad searches that return hundreds of irrelevant hits:

1. **Read the most recent 3–5 Discord log files** in each vault (`Discord/YYYY-MM-DD.md`).  
   These files are **synthesized agent reports**, not raw transcripts. They often contain:  
   - Executive summaries of who is doing what  
   - References to external links (Google Drive, Canva, Docs) where the actual file lives  
   - Deadlines and handoff notes  
   → *Start here before running keyword searches.*

2. **Scan for external platform references** inside those logs.  
   Typical patterns:  
   - `https://docs.google.com/document/d/...` (scripts, treatments, briefs)  
   - `https://www.canva.com/design/...` (pitch decks, one-pagers)  
   - `https://drive.google.com/drive/folders/...` (phối cảnh, reference boards)  
   - `https://docs.google.com/spreadsheets/...` (plans, timelines)  
   If a user says "Linh gửi kịch bản", the actual file is almost always on Drive/Canva and only the *link* is in the vault.

3. **Only then run targeted keyword searches** inside `TaiLieu-*` and `Báo cáo` folders.  
   Broad vault-wide keyword searches across all `Discord/` files usually produce 200+ noise hits because the logs are long and mention many names.

## Pitfalls

1. **BOM in markdown files**: Files written by Obsidian or exported from Discord may start with `\ufeff`. Reading with `utf-8` leaves the BOM as invisible junk at the start of the string; use `utf-8-sig` to strip it automatically.
2. **Missing date = no activity**: If `2026-06-04.md` does not exist in a vault's `Discord/` folder, that bộ phận had no logged Discord activity for that day. Do not treat as an error.
3. **Never use `read_file` or `terminal` for vault paths**: Even if the path looks simple, the tool layer on this Windows host is flaky with the `C:\Users\Admin\Documents\Obsidian Vault` tree. Stick to `execute_code` + Python for consistency.
4. **Vietnamese diacritics in filenames**: Filenames may contain Vietnamese characters (e.g. `Báo-cáo-tổng-hợp.md`). Python `os.listdir` handles these correctly; `read_file` does not.
5. **Discord logs are synthesized reports, not raw transcripts**: Do not search them as if they were verbatim chat logs. Look for summaries, action items, and external links rather than trying to grep every line.
6. **Actual deliverables live on external platforms**: Users (especially Creative and Content) share work via Google Drive, Canva, or Docs. The vault almost never contains the native file — only the link and context.
7. **Tool-layer latency after write**: If `write_file` succeeds but a subsequent `read_file` on the same path returns "File not found", the file does exist. Use `execute_code` + Python to verify (`os.path.exists`, `open(...)`) rather than retrying with `read_file`. The `read_file` tool may have stale directory cache on this Windows host.
8. **Anonymized Discord IDs (`<@***>`)**: Vault exports scrub user snowflakes into `<@***>` placeholders. If you need to resolve a user name, you **must** send a raw mention (`<@snowflake>`) into Discord via `send_message` and read the resolved display name from the resulting chat message. Searching the vault for the raw snowflake will yield zero readable hits.
9. **Cannot enumerate user's mutual servers**: The agent has no Discord administrative privileges. It cannot see which servers a given user belongs to, nor inspect member lists of arbitrary guilds. The only reliable server info is what the agent receives in-context (e.g., invite links opened via `browser_navigate`).

## References

- See `references/discord-log-structure.md` for a concrete example of how Discord logs are structured inside a daily file.
- See `references/extract-user-blocks-from-discord-logs.md` for the canonical pattern to reverse-engineer a user's implicit "plan" from scattered Discord messages — splitting by author block, filtering by topic keywords, and keeping only substantive blocks.
- See `references/vault-search-scripts.md` for ready-to-run Python scripts (recent logs, external-link extraction, person+deliverable search, recently-modified non-Discord files).
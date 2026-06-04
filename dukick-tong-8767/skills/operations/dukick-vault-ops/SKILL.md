---
name: dukick-vault-ops
description: >
  Reliable access to DuKick's 5 Obsidian vaults on the Windows host.
  Covers directory layout, Discord log file conventions, and the critical
  Windows-path workaround (use execute_code + Python instead of read_file/terminal).
triggers:
  - Need to read vault files from DuKick-Tong, DuKick-PM, DuKick-TruyenThong, DuKick-PMCreative, or DuKick-NeoLab
  - read_file or terminal fails on vault paths
  - Need to list, search, or parse Discord logs or Báo cáo files
---

# DuKick Vault Operations

## Vault Layout

All 5 vaults live under the same parent directory:

```
C:\Users\Admin\Documents\Obsidian Vault\
├── DuKick-Tong\          (Tổng — điều phối)
│   ├── Báo cáo\
│   ├── Discord\
│   └── README.md
├── DuKick-PM\            (Account)
│   ├── Discord\
│   ├── TaiLieu-Account\
│   └── README.md
├── DuKick-TruyenThong\   (Sales)
│   ├── Discord\
│   ├── TaiLieu-Sales\
│   └── README.md
├── DuKick-PMCreative\    (Creative)
│   ├── Discord\
│   ├── TaiLieu-Creative\
│   └── README.md
└── DuKick-NeoLab\        (Finance)
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

vault = r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-PM"
discord_dir = os.path.join(vault, "Discord")
files = sorted(os.listdir(discord_dir))   # already sorted by date string
latest = files[-1] if files else None
```

## ⚠️ CRITICAL: Windows Path Workaround

On this Windows host both `read_file` and `terminal` are **unreliable** for vault paths:

| Tool | Failure mode |
|------|-------------|
| `read_file` | "File not found" on paths containing spaces or Vietnamese characters (e.g. `Báo cáo`, `Tài liệu`) |
| `terminal` | WSL not installed → every shell command errors out |

**Always use `execute_code` with Python** for vault file I/O.

### Read a vault file

```python
import os

path = r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-Tong\Báo cáo\2026-06-03_Báo-cáo-tổng-hợp.md"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()
print(content[:2000])
```

### List a directory

```python
import os

dir_path = r"C:\Users\Admin\Documents\Obsidian Vault\DuKick-PM\TaiLieu-Account"
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
    "Tong": "DuKick-Tong",
    "PM": "DuKick-PM",
    "TruyenThong": "DuKick-TruyenThong",
    "PMCreative": "DuKick-PMCreative",
    "NeoLab": "DuKick-NeoLab",
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
| DuKick-Tong | `Báo cáo` | Báo cáo tổng hợp định kỳ (agent-generated) |
| DuKick-PM | `TaiLieu-Account` | SOP, case study, tài liệu nghiệp vụ Account |
| DuKick-TruyenThong | `TaiLieu-Sales` | Elevator pitch, email mẫu, list câu hỏi sale |
| DuKick-PMCreative | `TaiLieu-Creative` | Quy trình creative, treatment |
| DuKick-NeoLab | `TaiLieu-Finance` | Hợp đồng mẫu, quy trình chứng từ, tạm ứng |

## Pitfalls

1. **BOM in markdown files**: Files written by Obsidian or exported from Discord may start with `\ufeff`. Reading with `utf-8` leaves the BOM as invisible junk at the start of the string; use `utf-8-sig` to strip it automatically.
2. **Missing date = no activity**: If `2026-06-04.md` does not exist in a vault's `Discord/` folder, that bộ phận had no logged Discord activity on that day. Do not treat as an error.
3. **Never use `read_file` or `terminal` for vault paths**: Even if the path looks simple, the tool layer on this Windows host is flaky with the `C:\Users\Admin\Documents\Obsidian Vault` tree. Stick to `execute_code` + Python for consistency.
4. **Vietnamese diacritics in filenames**: Filenames may contain Vietnamese characters (e.g. `Báo-cáo-tổng-hợp.md`). Python `os.listdir` handles these correctly; `read_file` does not.

## References

- See `references/discord-log-structure.md` for a concrete example of how Discord logs are structured inside a daily file.

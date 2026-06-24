# Reference: Concrete Search Scripts for Dukick Vaults

Scripts below are designed to be dropped into `execute_code` when the Tổng agent needs to find a specific deliverable or person across the 5 vaults.

## Script 1: Read recent Discord logs across all vaults

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

def read_latest_discord(vault_name, n=3):
    discord_dir = os.path.join(VAULT_ROOT, vaults[vault_name], "Discord")
    if not os.path.isdir(discord_dir):
        return []
    files = sorted(os.listdir(discord_dir))
    return files[-n:]

for name in vaults:
    latest = read_latest_discord(name, n=3)
    print(f"{name}: {latest}")
```

## Script 2: Find external platform links in recent logs

```python
import os, re

VAULT_ROOT = r"C:\Users\Admin\Documents\Obsidian Vault"
vaults = ["Dukick-Tong","Dukick-PM","Dukick-TruyenThong","Dukick-PMCreative","Dukick-NeoLab"]

link_pattern = re.compile(
    r'https?://(?:docs\.google\.com|drive\.google\.com|www\.canva\.com)/[^\s\)>\]]+',
    re.IGNORECASE
)

for v in vaults:
    discord_dir = os.path.join(VAULT_ROOT, v, "Discord")
    if not os.path.isdir(discord_dir):
        continue
    files = sorted(os.listdir(discord_dir))[-5:]  # last 5 days
    for f in files:
        path = os.path.join(discord_dir, f)
        try:
            with open(path, "r", encoding="utf-8-sig") as fh:
                text = fh.read()
        except Exception:
            continue
        matches = link_pattern.findall(text)
        if matches:
            print(f"--- {v} / {f} ---")
            for m in matches[:10]:
                print(m)
            print()
```

## Script 3: Search for a person + deliverable keyword in recent logs

```python
import os

VAULT_ROOT = r"C:\Users\Admin\Documents\Obsidian Vault"
vaults = ["Dukick-Tong","Dukick-PM","Dukick-TruyenThong","Dukick-PMCreative","Dukick-NeoLab"]

person = "linh"          # name to search
deliverable = "kịch bản" # or script, treatment, brief, idea

days_back = 14

import time
now = time.time()
cutoff = now - days_back * 86400

for v in vaults:
    discord_dir = os.path.join(VAULT_ROOT, v, "Discord")
    if not os.path.isdir(discord_dir):
        continue
    files = sorted(os.listdir(discord_dir))
    for f in files:
        path = os.path.join(discord_dir, f)
        try:
            mtime = os.path.getmtime(path)
            if mtime < cutoff:
                continue
            with open(path, "r", encoding="utf-8-sig") as fh:
                text = fh.read()
        except Exception:
            continue
        low = text.lower()
        if person in low and deliverable in low:
            print(f"=== {v} / {f} ===")
            # Print matching lines with context
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if person in line.lower() and deliverable in line.lower():
                    start = max(0, i - 3)
                    end = min(len(lines), i + 6)
                    print("\n".join(lines[start:end]))
                    print("---")
            print()
```

## Script 4: List recently-modified non-Discord files (TaiLieu / Báo cáo)

```python
import os, time

VAULT_ROOT = r"C:\Users\Admin\Documents\Obsidian Vault"
vaults = ["Dukick-Tong","Dukick-PM","Dukick-TruyenThong","Dukick-PMCreative","Dukick-NeoLab"]

now = time.time()
cutoff = now - 2 * 86400  # last 2 days

for v in vaults:
    root = os.path.join(VAULT_ROOT, v)
    if not os.path.isdir(root):
        continue
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        if "Discord" in dirpath:
            continue
        for f in filenames:
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            try:
                mtime = os.path.getmtime(path)
                if mtime >= cutoff:
                    hits.append((path, mtime))
            except Exception:
                pass
    if hits:
        print(f"=== {v} ({len(hits)} files) ===")
        for p, mt in sorted(hits, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {time.strftime('%Y-%m-%d %H:%M', time.localtime(mt))}  {os.path.basename(p)}")
        print()
```

## Key takeaway

Always run **Script 1 + Script 2 first** (recent logs + external links) before broad keyword searches. This avoids 200+ noise hits and quickly surfaces where the actual deliverable lives (Drive, Canva, Docs).
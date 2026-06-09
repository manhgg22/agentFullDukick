# Reference: Extracting a Specific User's Messages from Discord Logs

When the leader asks for "plan của user X" or "extract what user Y said", the Discord logs are the primary source. Use this script pattern inside `execute_code`.

## The pattern

Discord log files are markdown with `### HH:MM — Author` delimiters. The most robust extraction is:

1.  Split the file on `\n### ` to isolate message blocks.
2.  Filter blocks containing the target user name.
3.  Further filter by strategic/AI/plan keywords if needed.
4.  Keep the longest blocks ( >150 chars ) — those are substantive messages, not emoji reactions or short replies.

## Script: Extract all substantive messages from a user

```python
import os, re, glob

path = r'C:\Users\Admin\Documents\Obsidian Vault\DuKick-Tong\Discord'
files = sorted(glob.glob(os.path.join(path, '*.md')), key=os.path.getmtime, reverse=True)

target_user = 'phamgianam'   # change as needed

all_blocks = []
for fp in files:
    with open(fp, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    blocks = re.split(r'\n### ', content)
    for block in blocks:
        if re.search(target_user, block, re.I):
            date = os.path.basename(fp).replace('.md', '')
            all_blocks.append({'date': date, 'block': block.strip()})

# Keep only substantive blocks (>150 chars) to skip emoji reactions / "ok" / image-only posts
substantive = [b for b in all_blocks if len(b['block']) > 150]

print(f"Found {len(substantive)} substantive blocks")
for b in substantive[:30]:
    print(f"\n=== {b['date']} ===")
    print(b['block'][:1200])
```

## Script: Filter further by strategic keywords

After extracting all blocks from the user, narrow down to AI / strategy / planning content:

```python
import re

keywords = r'agent|AI|bot|system|hermes|c-level|mô hình|code|discord|lark|train|nhúng|update.*agent|toàn bộ|BOD|trợ lý|mẹ ở mọi nơi|final.*agent|workflow|automation|chuyển đổi|tổ chức|positioning|định hướng|triển khai.*agent|tất cả.*agent|agent.*mọi nơi|toàn bộ.*agent|AI hóa|agent hóa'

filtered = []
for item in all_blocks:
    if re.search(keywords, item['block'], re.I):
        filtered.append(item)

for b in filtered:
    if len(b['block']) > 150:
        print(f"\n=== {b['date']} ===")
        print(b['block'][:1500])
```

## Why this matters

- Discord logs are **synthesized agent reports**, not raw chat transcripts. The `###` blocks are already grouped by author.
- Broad keyword searches across the whole file often return 400+ hits because names appear in many contexts (e.g. "check job của a Nam").
- Splitting by author first isolates **who** said it, then filtering by topic isolates **what** they said about the topic.
- This is the canonical way to reverse-engineer a "plan" that a user has expressed implicitly across many messages, rather than in a single document.

## Pitfall: Image-only or voice-message posts

Many Discord blocks contain only attachment links (e.g. `📎 [image.png](...)` or `📎 [voice-message.ogg](...)`). These blocks are **short** (<150 chars after stripping markdown). Filtering by `len(block) > 150` naturally drops them. If the attachment is strategic (screenshot of a plan), the user usually adds context text — which keeps the block long.

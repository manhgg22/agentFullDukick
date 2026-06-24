# Fix Cron Database BOM Corruption

## Symptom
`cronjob(action='list')` returns:
```
Cron database corrupted and unrepairable: Unexpected UTF-8 BOM (decode using utf-8-sig)
```

## Root cause
`jobs.json` in `C:\DukickAgent\Dukick-tong-8767\cron\` has a UTF-8 BOM (`\xef\xbb\xbf`) prepended.

## Fix (Python script)

```python
import os

cron_path = r"C:\DukickAgent\Dukick-tong-8767\cron\jobs.json"

with open(cron_path, 'rb') as f:
    content = f.read()

if content[:3] == b'\xef\xbb\xbf':
    with open(cron_path, 'wb') as f:
        f.write(content[3:])
    print("BOM removed successfully")
else:
    print("No BOM found")
```

## Why not use utf-8-sig?
Reading with `utf-8-sig` encoding strips BOM transparently, but writing back with normal `utf-8` can re-add BOM depending on the environment. The binary cut approach is deterministic and safe.

## Prevention
- Do not use `echo` or heredoc with UTF-8 BOM characters to write cron files
- When creating cron jobs programmatically, always write with `encoding='utf-8'` (no sig)

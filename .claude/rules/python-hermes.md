---
description: "Python rules cho Hermes agent codebase"
globs: ["**/*.py", "save_to_obsidian.py", "Dukick-*/**/*.py"]
alwaysApply: false
---

# Python Rules — Hermes/Dukick

## Môi trường

- Interpreter: `C:/DukickAgent/venv/Scripts/python.exe`
- Luôn dùng `from __future__ import annotations` ở đầu file
- Type hints bắt buộc trên mọi function

## Encoding

```python
# LUÔN chỉ định encoding khi đọc/ghi file
with open(path, "r", encoding="utf-8") as f: ...
with open(path, "a", encoding="utf-8") as f: ...
```

## Path handling

```python
from pathlib import Path   # dùng Path, không dùng os.path
vault = Path(r"C:\Users\Admin\Documents\Obsidian Vault")
folder = vault / "Dukick-Tong" / "Discord"
folder.mkdir(parents=True, exist_ok=True)
```

## Hook scripts (pre_gateway_dispatch)

- Đọc JSON từ `sys.stdin`
- Luôn `print(json.dumps({"action": "allow"}))` khi xử lý xong
- Timeout tối đa 5 giây — KHÔNG làm tác vụ nặng trong hook
- Không raise exception — dùng `sys.exit(0)` khi có lỗi để không chặn bot

## Hermes config (YAML)

```yaml
# config.yaml của mỗi agent
discord:
  require_mention: true
  auto_thread: false

hooks:
  pre_gateway_dispatch:
    - command: "python path/to/script.py"
      timeout: 5
```

## Error handling trong hooks

```python
try:
    payload = json.loads(raw)
except json.JSONDecodeError:
    sys.exit(0)  # thoát êm, không crash bot
```

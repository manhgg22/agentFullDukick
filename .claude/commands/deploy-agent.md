---
name: deploy-agent
description: Khởi động hoặc restart một hoặc tất cả Hermes Discord agents
allowed_tools: ["Bash", "Read", "Write", "Glob"]
---

# /deploy-agent

Dùng lệnh này để **khởi động, restart, hoặc kiểm tra** trạng thái 5 Hermes Discord agents.

## Agents có sẵn

| Tên | Port | Start script |
|---|---|---|
| `tong` | 8767 | `start-dukick-tong-8767.bat` |
| `truyenthong` | 8768 | `start-dukick-truyenthong-8768.bat` |
| `pm` | 8769 | `start-dukick-pm-8769.bat` |
| `pmcreative` | 8770 | `start-dukick-pmcreative-8770.bat` |
| `neolab` | 8771 | `start-dukick-neolab-8771.bat` |

## Sequence

### 1. Kiểm tra .env trước khi deploy

Mỗi agent cần có trong `.env`:
```
DISCORD_BOT_TOKEN=<token>
```

Kiểm tra: đọc file `.env` của agent được chỉ định và xác nhận token tồn tại (không rỗng, không phải placeholder).

### 2. Kiểm tra config.yaml

Xác nhận `discord.require_mention: true` và `auto_thread: false` đang đúng.

### 3. Khởi động agent

Chạy start script tương ứng:
```
C:\DuKickAgent\start-dukick-{tên}-{port}.bat
```

Hoặc dùng PowerShell:
```powershell
$env:HERMES_HOME = "C:/DuKickAgent/dukick-{tên}-{port}"
C:/DuKickAgent/venv/Scripts/python.exe -m hermes_cli.main gateway run --replace
```

### 4. Xác nhận đang chạy

Kiểm tra file `gateway_state.json` trong thư mục agent:
```json
{"gateway_state": "running", ...}
```

## Notes

- Khởi động `tong` **sau cùng** vì nó coordinator, cần các agent khác online trước
- Nếu agent đang chạy, `--replace` sẽ tự restart an toàn
- Logs nằm tại `dukick-{tên}-{port}/logs/`

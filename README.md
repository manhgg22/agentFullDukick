# DuKick Agent System

## Giới thiệu
5 AI Discord agents cho các bộ phận DuKick: Tổng, Sales, Account, Creative, Finance.

## Yêu cầu hệ thống
- Windows 10+
- Python 3.10+ (venv tại C:/DuKickAgent/venv)
- Discord account + 5 bot tokens
- Obsidian (cài tại C:/Users/Admin/AppData/Local/Programs/Obsidian)

## Cài đặt

### Bước 1: Cấu hình Discord token
Mỗi agent cần file .env với DISCORD_BOT_TOKEN:
```
C:\DuKickAgent\dukick-tong-8767\.env       → Bot Tổng
C:\DuKickAgent\dukick-truyenthong-8768\.env → Bot Sales
C:\DuKickAgent\dukick-pm-8769\.env          → Bot Account
C:\DuKickAgent\dukick-pmcreative-8770\.env  → Bot Creative
C:\DuKickAgent\dukick-neolab-8771\.env      → Bot Finance
```
Nội dung .env: DISCORD_BOT_TOKEN=your_token_here

### Bước 2: Bật Discord bot intents
Trong Discord Developer Portal, mỗi bot cần bật:
- Message Content Intent
- Server Members Intent
- Presence Intent

### Bước 3: Mời bot vào Discord server
Dùng OAuth2 URL Generator với scope: bot + permissions: Send Messages, Read Message History, View Channels

### Bước 4: Khởi động agents (thứ tự quan trọng)
```bat
start-dukick-truyenthong-8768.bat
start-dukick-pm-8769.bat
start-dukick-pmcreative-8770.bat
start-dukick-neolab-8771.bat
rem Khởi động Tổng Agent SAU CÙNG
start-dukick-tong-8767.bat
```

### Bước 5: Kiểm tra bot online
Kiểm tra gateway_state.json: "gateway_state": "running"

## Cấu trúc thư mục

```
C:\DuKickAgent\
├── dukick-tong-8767\          # Bot Tổng — điều phối toàn bộ hệ thống
│   ├── bot.py
│   ├── config.yaml
│   ├── gateway_state.json
│   └── .env
├── dukick-truyenthong-8768\   # Bot Sales — truyền thông & marketing
│   ├── bot.py
│   ├── config.yaml
│   ├── gateway_state.json
│   └── .env
├── dukick-pm-8769\            # Bot Account — quản lý tài khoản & dự án
│   ├── bot.py
│   ├── config.yaml
│   ├── gateway_state.json
│   └── .env
├── dukick-pmcreative-8770\    # Bot Creative — sáng tạo nội dung
│   ├── bot.py
│   ├── config.yaml
│   ├── gateway_state.json
│   └── .env
├── dukick-neolab-8771\        # Bot Finance — tài chính & kế toán
│   ├── bot.py
│   ├── config.yaml
│   ├── gateway_state.json
│   └── .env
├── shared\                    # File dùng chung giữa các agent
│   ├── save_to_obsidian.py    # Module lưu ghi chú vào Obsidian vault
│   ├── ecc_config.json        # Cấu hình ECC (Event/Command/Config)
│   └── utils.py
├── venv\                      # Python virtual environment
├── start-dukick-tong-8767.bat
├── start-dukick-truyenthong-8768.bat
├── start-dukick-pm-8769.bat
├── start-dukick-pmcreative-8770.bat
├── start-dukick-neolab-8771.bat
└── README.md
```

**Obsidian vault** mặc định: `C:\Users\Admin\Documents\DuKick-Notes`
Được cấu hình trong `shared\save_to_obsidian.py` — thay đổi `VAULT_PATH` nếu cần.

**ECC config** (`shared\ecc_config.json`): định nghĩa các event routing giữa các bot,
cho phép Bot Tổng điều phối lệnh tới các bot chuyên biệt.

## Troubleshooting
- **Bot không online**: kiểm tra DISCORD_BOT_TOKEN trong .env
- **Bot không phản hồi**: kiểm tra Message Content Intent đã bật chưa
- **Obsidian không lưu**: kiểm tra vault path trong save_to_obsidian.py
- **YAML error**: kiểm tra config.yaml có đúng indentation không
- **Python error**: kiểm tra venv tại C:/DuKickAgent/venv

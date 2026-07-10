# Dukick Agent System

Hệ thống **8 AI agent** chạy song song phục vụ nội bộ công ty Dukick — gồm Discord bots và bot Zalo thu nợ.

---

## Agents

| Agent | Port | Tên hiển thị | Vai trò |
|---|---|---|---|
| `dukick-tong-8767` | 8767 | **CEO Assistant** | Trợ lý riêng CEO — tổng hợp thông tin toàn công ty, hỗ trợ ra quyết định |
| `dukick-truyenthong-8768` | 8768 | Sales Agent | Lead, pipeline, pitching, handoff sang PM |
| `dukick-pm-8769` | 8769 | Account Agent | Quản lý dự án, timeline, tiến độ |
| `dukick-pmcreative-8770` | 8770 | Creative Agent | Giám sát sản xuất, reference, chất lượng sáng tạo |
| `dukick-ketoan-8771` | 8771 | Finance Agent | Thu chi, công nợ, quyết toán, báo cáo |
| `hermes-hr-8772` | 8772 | HR Agent | Quản lý nhân sự |
| `dukick-thuno-8773` | 8773 | Thu nợ Agent | Bot Zalo — nhắc lịch thanh toán khách hàng (port 8889) |
| `dukick-huy-8774` | 8774 | Hỗ trợ Agent | Vận hành nội bộ |

---

## Khởi động

```powershell
# Khởi động tất cả
start-all-agents.bat

# Khởi động từng agent
start-dukick-tong-8767.bat        # CEO Assistant — khởi động SAU CÙNG
start-dukick-truyenthong-8768.bat
start-dukick-pm-8769.bat
start-dukick-pmcreative-8770.bat
start-dukick-ketoan-8771.bat
start-hermes-hr-8772.bat
start-dukick-thuno-8773.bat       # Bot Zalo (webhook port 8889)
start-dukick-huy-8774.bat

# Tắt agent (đọc PID từ gateway.pid)
Stop-Process -Id (Get-Content agents\dukick-huy-8774\gateway.pid | ConvertFrom-Json).pid -Force
```

---

## Cấu trúc thư mục

```
C:\DuKickAgent\
├── agents\
│   ├── dukick-tong-8767\          ← CEO Assistant
│   │   ├── SOUL.md                ← Nhân cách + vai trò
│   │   ├── config.yaml            ← Discord config
│   │   └── .env                   ← DISCORD_BOT_TOKEN (không commit)
│   ├── dukick-truyenthong-8768\
│   ├── dukick-pm-8769\
│   ├── dukick-pmcreative-8770\
│   ├── dukick-ketoan-8771\
│   ├── hermes-hr-8772\
│   ├── dukick-thuno-8773\         ← Bot Zalo
│   │   ├── debt_data\debts.json   ← 75 khoản công nợ
│   │   └── scripts\               ← webhook_server.py, reminder_scheduler.py
│   └── dukick-huy-8774\
├── shared\                        ← Utilities dùng chung (upload_to_drive, gauth...)
├── docs\                          ← Tài liệu hệ thống
├── venv\                          ← Python virtualenv
└── save_to_obsidian.py            ← Hook auto-save Discord → Obsidian
```

---

## Quy tắc tuyệt đối

- ❌ KHÔNG commit `.env` — chứa Discord bot token
- ❌ Bot KHÔNG tự duyệt ngân sách, chốt giá, xác nhận chất lượng cuối, gửi báo cáo tài chính
- ✅ Discord bots chỉ trả lời khi được **@tag** (`require_mention: true`)
- ✅ Khởi động **CEO Assistant sau cùng**
- ✅ Mọi quyết định quan trọng cần người có thẩm quyền xác nhận

---

## Bot Zalo — agentThuno

Bot riêng chạy song song, không phải Discord. Webhook tại `http://localhost:8889`.

```
# Kiểm tra bot đang chạy
curl http://localhost:8889/health

# Lệnh admin qua Zalo chat
/help              → danh sách lệnh
/debts <tên>       → tra cứu công nợ theo khách/project
/list overdue      → khoản quá hạn
/paid DEBT-0005    → đánh dấu đã thanh toán
/setid <id> <DEBT-xxx,DEBT-xxx>  → gán Zalo ID cho khách
```

---

## Obsidian Vault

Mọi tin nhắn Discord được tự động lưu vào:
```
C:\Users\Admin\Documents\Obsidian Vault\
├── Dukick-Tong\       ← CEO Assistant đọc vault này
├── Dukick-TruyenThong\
├── Dukick-PM\
├── Dukick-PMCreative\
└── Dukick-NeoLab\
```

---

## Git

```
Remote: https://github.com/manhgg22/agentFullDukick
Branch: main
```

Không commit: `*.env`, `*.db`, `*.pid`, `*/sessions/`

# TÀI LIỆU HỆ THỐNG — DUKICK AGENT SYSTEM
**Phiên bản:** 1.0 | **Ngày tạo:** 2026-07-10 | **Người chịu trách nhiệm:** Mạnh (manhgg22)

---

## MỤC LỤC

1. [Hệ thống là gì?](#1-hệ-thống-là-gì)
2. [Ai sử dụng?](#2-ai-sử-dụng)
3. [Dùng khi nào?](#3-dùng-khi-nào)
4. [Dùng như thế nào?](#4-dùng-như-thế-nào)
5. [Dữ liệu đi đâu?](#5-dữ-liệu-đi-đâu)
6. [Ai chịu trách nhiệm?](#6-ai-chịu-trách-nhiệm)
7. [Hệ thống KHÔNG được phép làm gì?](#7-hệ-thống-không-được-phép-làm-gì)
8. [Kiến trúc kỹ thuật](#8-kiến-trúc-kỹ-thuật)
9. [Hướng dẫn khởi động / vận hành](#9-hướng-dẫn-khởi-động--vận-hành)
10. [Xử lý sự cố thường gặp](#10-xử-lý-sự-cố-thường-gặp)

---

## 1. Hệ thống là gì?

**Dukick Agent System** là hệ thống **AI tự động phục vụ nội bộ công ty Dukick** gồm 2 phần:

### Phần A — Bot Zalo nhắc lịch thanh toán (agentThuno)

Bot Zalo AI tên **Dukick Agent Service**, chạy tại port `8889`.

**Làm gì:**
- Tự động nhắn tin Zalo nhắc khách hàng về lịch thanh toán theo hợp đồng
- Trả lời câu hỏi về công nợ, số tiền, ngày dự kiến khi khách hỏi
- Cho phép admin tra cứu, cập nhật trạng thái thanh toán qua Zalo

**Không làm gì:**
- Không đòi nợ theo nghĩa tiêu cực — chỉ "nhắc lịch thanh toán"
- Không tự xóa/giảm tiền, không cam kết gia hạn

---

### Phần B — Discord Agents (8 bot nội bộ)

8 bot AI chạy song song trên Discord nội bộ Dukick, mỗi bot phụ trách 1 bộ phận:

| Bot | Port | Vai trò | Nhiệm vụ |
|---|---|---|---|
| **dukick-tong** | 8767 | Coordinator | Điều phối toàn hệ thống, đọc tất cả vault |
| **dukick-pm** | 8769 | Account/PM | Quản lý dự án, timeline, tiến độ |
| **dukick-pmcreative** | 8770 | Creative PM | Giám sát sản xuất, reference, chất lượng |
| **dukick-truyenthong** | 8768 | Sales | Lead, pipeline, pitching, handoff |
| **dukick-ketoan** | 8771 | Kế toán | Thu chi, công nợ, quyết toán, báo cáo |
| **dukick-huy** | 8774 | Hỗ trợ | Hỗ trợ nhân sự/vận hành |
| **hermes-hr** | 8772 | HR | Quản lý nhân sự |
| **dukick-thuno** | 8773 | Thu nợ | Bot Zalo — xem Phần A |

> Các bot Discord **chỉ trả lời khi bị @tag** — không tự chạy nền.

---

## 2. Ai sử dụng?

### Bot Zalo (agentThuno)

| Người dùng | Quyền | Dùng để |
|---|---|---|
| **Khách hàng Dukick** | Chỉ xem thông tin của mình | Hỏi về lịch thanh toán, xác nhận đã chuyển |
| **Kế toán Dukick** | Admin đầy đủ | Tra cứu toàn bộ, gán Zalo ID, cập nhật trạng thái |
| **Quản lý Dukick** | Admin đầy đủ | Xem báo cáo tổng hợp, theo dõi công nợ |

### Discord Agents

| Người dùng | Cách dùng |
|---|---|
| **Nhân viên Dukick** | @tag bot liên quan trong kênh Discord tương ứng |
| **Leader/Manager** | @tag dukick-tong để tổng hợp thông tin cross-bộ phận |

---

## 3. Dùng khi nào?

### Bot Zalo — agentThuno

**Tự động (không cần người điều khiển):**
- Mỗi sáng 8h → scheduler tự quét debts.json → nhắn Zalo cho khách có khoản quá hạn hoặc sắp đến hạn (trong 3 ngày)

**Thủ công (khi cần):**
- Kế toán muốn tra cứu khoản của một khách cụ thể
- Kế toán muốn đánh dấu khoản đã thanh toán
- Kế toán muốn gán Zalo ID cho khách để bật tự động nhắc
- Import dữ liệu mới từ Excel

### Discord Agents

- Khi nhân viên cần hỏi bot về dự án, deadline, brief, công nợ, sản xuất
- Khi cần bot tổng hợp thông tin từ nhiều bộ phận
- Khi cần nhắc việc, cảnh báo rủi ro, tạo checklist/báo cáo

---

## 4. Dùng như thế nào?

### 4A. Khách hàng dùng Bot Zalo

Khách hàng nhắn tin bình thường vào Zalo OA (Official Account) của Dukick:

```
"Cho tôi biết khoản thanh toán đợt 2 của project HNS là bao nhiêu?"
→ Bot tự trả lời dựa trên debts.json
```

---

### 4B. Admin/Kế toán dùng lệnh Zalo

Mở Zalo OA → nhắn lệnh vào chat:

#### Xem danh sách lệnh
```
/help
```

#### Tra cứu công nợ theo tên khách/project
```
/debts The One
→ Hiện tất cả khoản của "The One": ID, số tiền, ngày hạn, Zalo ID đã gán chưa

/debts HNS
→ Tìm tất cả khoản chứa "HNS"
```

#### Xem danh sách theo trạng thái
```
/list overdue   → Khoản chưa nhận xác nhận (đã qua ngày dự kiến)
/list pending   → Khoản sắp đến hạn
/list all       → Toàn bộ 75 khoản
```
> Nếu danh sách dài → bot tự gửi nhiều tin (mỗi tin 20 khoản)

#### Tra cứu theo Zalo ID
```
/check 4a6f8b15bb40521e0b51
→ Hiện tên khách + toàn bộ khoản của người có Zalo ID đó

/check
→ Tra cứu chính người đang nhắn
```

#### Gán Zalo ID cho khách (để bật nhắc tự động)
```
/setid 4a6f8b15bb40521e0b51 DEBT-0005,DEBT-0006,DEBT-0007
→ Gán Zalo ID của khách vào 3 khoản đó
→ Từ hôm sau, scheduler sẽ tự nhắc khách này
```

> **Lấy Zalo ID ở đâu?**
> Vào lịch sử chat Zalo OA → chọn khách → copy User ID từ thông tin khách.

#### Đánh dấu khoản đã thanh toán
```
/paid DEBT-0005 da chuyen 03/07
→ Cập nhật status = paid trong debts.json
→ Tự động sync lên Google Sheet
```

---

### 4C. Quy trình gán Zalo ID (lần đầu cho khách mới)

1. Nhắn `/debts <tên khách>` → lấy danh sách DEBT-xxxx
2. Vào Zalo OA → lịch sử chat → lấy Zalo user ID của khách
3. Nhắn `/setid <zalo_id> <DEBT-xxx,DEBT-xxx>`
4. Hôm sau scheduler tự nhắc

---

### 4D. Import dữ liệu từ Excel

Khi có file `sheet_2.xlsx` mới:
```powershell
C:/DukickAgent/venv/Scripts/python.exe agents/dukick-thuno-8773/scripts/import_excel.py
```
> **Cảnh báo:** Lệnh này **ghi đè toàn bộ** debts.json. Chạy xong phải gán lại Zalo ID nếu cần.

---

### 4E. Dùng Discord Agents

Trong kênh Discord tương ứng → @tag bot:

```
@dukick-pm Dự án HNS đang ở giai đoạn nào?
@dukick-ketoan Tổng công nợ tháng 7 là bao nhiêu?
@dukick-tong Tóm tắt tình hình tuần này cho tôi
```

> Bot **không trả lời** nếu không có @tag.

---

## 5. Dữ liệu đi đâu?

### Luồng dữ liệu Bot Zalo

```
Tin nhắn Zalo của khách
        ↓
Zalo Bot Platform (webhook POST)
        ↓
webhook_server.py (port 8889)
        ↓
[Lưu log] → debt_data/webhook_logs.jsonl
        ↓
[Nếu là lệnh /...] → xử lý trực tiếp → reply Zalo
[Nếu là câu hỏi thường] → gọi AI (ollama/openai) → reply Zalo
        ↓
[Nếu /paid] → cập nhật debts.json → sync Google Sheet
```

### Luồng nhắc tự động

```
Mỗi sáng 8h (Windows Task Scheduler)
        ↓
reminder_scheduler.py chạy
        ↓
Đọc debts.json → lọc khoản: overdue + pending (trong 3 ngày)
        ↓
Với mỗi khoản có contact_phone → gửi Zalo
        ↓
Cập nhật reminder_count, last_reminder trong debts.json
```

### Luồng dữ liệu Discord Agents

```
Tin nhắn Discord (có @tag)
        ↓
Hermes agent nhận (port 8767-8774)
        ↓
Gọi AI → trả lời Discord
        ↓
Hook pre_gateway_dispatch → save_to_obsidian.py
        ↓
Lưu vào Obsidian Vault (C:\Users\Admin\Documents\Obsidian Vault\Dukick-{TenAgent}\)
```

### Các kho dữ liệu

| Dữ liệu | Vị trí | Ghi chú |
|---|---|---|
| Công nợ (75 khoản) | `agents/dukick-thuno-8773/debt_data/debts.json` | File chính, nguồn sự thật |
| Google Sheet đồng bộ | Sheet ID: `1GiGuwNGZ2PWdtpjrimdr0nBkOZBZl2Zm743-KndIcRY` | Sync 2 chiều qua sync_sheets.py |
| Log webhook Zalo | `debt_data/webhook_logs.jsonl` | Tất cả tin nhắn đến |
| Config Zalo bot | `debt_data/zalo_config.json` | bot_token, secret_token |
| Lịch sử Discord | Obsidian Vault mỗi agent | Auto-save mọi tin nhắn |
| Credentials | `.env` (mỗi agent) | **KHÔNG commit git** |

---

## 6. Ai chịu trách nhiệm?

| Hạng mục | Người chịu trách nhiệm |
|---|---|
| Vận hành hệ thống, khởi động bot | **Dev/Admin (Mạnh)** |
| Dữ liệu công nợ (debts.json) | **Kế toán Dukick** |
| Gán Zalo ID cho khách | **Kế toán Dukick** |
| Đánh dấu thanh toán (/paid) | **Kế toán Dukick** |
| Điều chỉnh số tiền, gia hạn, xóa khoản | **Kế toán Dukick** (thủ công, không qua bot) |
| Xác nhận chất lượng sản phẩm cuối | **PM Creative + Leader** |
| Chốt giá, ký hợp đồng | **Leader Dukick** |
| Gửi báo cáo tài chính chính thức | **Kế toán Dukick** (không qua bot) |
| Quyết định ngân sách | **Leader Dukick** |

> **Nguyên tắc:** Bot chỉ **hỗ trợ thông tin** — mọi quyết định quan trọng phải do **người có thẩm quyền** xác nhận.

---

## 7. Hệ thống KHÔNG được phép làm gì?

### Bot Zalo (agentThuno)

| Hành động | Lý do cấm |
|---|---|
| ❌ Tự xóa khoản công nợ | Ảnh hưởng sổ sách tài chính |
| ❌ Tự giảm số tiền | Chỉ kế toán được quyết định |
| ❌ Cam kết gia hạn với khách | Cần leader phê duyệt |
| ❌ Gửi báo cáo tài chính chính thức | Cần kế toán ký xác nhận |
| ❌ Dùng từ "đòi nợ", "nợ xấu", "quá hạn" | Ảnh hưởng quan hệ đối tác |
| ❌ Tự tạo khoản mới | Dữ liệu phải từ Excel/kế toán |

### Discord Agents (tất cả bot)

| Hành động | Lý do cấm |
|---|---|
| ❌ Tự duyệt ngân sách | Cần leader phê duyệt |
| ❌ Xác nhận chất lượng sản phẩm cuối cùng | Cần PM + leader review |
| ❌ Chốt giá với khách | Chỉ Sales + leader quyết định |
| ❌ Gửi báo cáo tài chính | Chỉ kế toán gửi chính thức |
| ❌ Cam kết với khách hàng bên ngoài | Cần người có thẩm quyền |
| ❌ Tự tạo thread Discord | `auto_thread: false` |
| ❌ Trả lời khi không được @tag | `require_mention: true` |

---

## 8. Kiến trúc kỹ thuật

### Cấu trúc thư mục

```
C:\DuKickAgent\
├── agents/
│   ├── dukick-thuno-8773/          ← Bot Zalo
│   │   ├── SOUL.md                 ← Nhân cách AI
│   │   ├── HUONG_DAN_SU_DUNG.md   ← Hướng dẫn người dùng
│   │   ├── .env                    ← API keys (KHÔNG commit)
│   │   ├── debt_data/
│   │   │   ├── debts.json          ← DỮ LIỆU CHÍNH 75 khoản
│   │   │   ├── zalo_config.json    ← Bot token Zalo
│   │   │   └── webhook_logs.jsonl  ← Log tất cả tin nhắn
│   │   └── scripts/
│   │       ├── webhook_server.py   ← Server chính (Flask, port 8889)
│   │       ├── reminder_scheduler.py ← Nhắc tự động
│   │       ├── import_excel.py     ← Import từ sheet_2.xlsx
│   │       └── sync_sheets.py      ← Đồng bộ Google Sheet
│   │
│   ├── dukick-tong-8767/           ← Discord Coordinator
│   ├── dukick-pm-8769/             ← Discord PM
│   ├── dukick-pmcreative-8770/     ← Discord Creative
│   ├── dukick-truyenthong-8768/    ← Discord Sales
│   ├── dukick-ketoan-8771/         ← Discord Finance
│   ├── dukick-huy-8774/            ← Discord Support
│   └── hermes-hr-8772/             ← Discord HR
│
├── venv/                           ← Python virtualenv
├── save_to_obsidian.py             ← Hook Discord → Obsidian
├── start-dukick-thuno-8773.bat     ← Khởi động bot Zalo
├── start-all-agents.bat            ← Khởi động tất cả
└── sheet_2.xlsx                    ← File Excel nguồn
```

### Stack công nghệ

| Thành phần | Công nghệ |
|---|---|
| Bot Zalo server | Python Flask, port 8889 |
| AI engine | OpenAI-compatible API (ollama/glm-5.2 hoặc cloud) |
| Discord bots | Hermes CLI framework |
| Dữ liệu chính | JSON file (debts.json) |
| Đồng bộ cloud | Google Sheets API |
| Auto-save | Obsidian Vault (Markdown) |
| Scheduler | Windows Task Scheduler |
| Runtime | Python 3.x (venv tại C:\DuKickAgent\venv\) |

---

## 9. Hướng dẫn khởi động / vận hành

### Khởi động Bot Zalo

```powershell
# Cách 1 — dùng file bat
C:\DuKickAgent\start-dukick-thuno-8773.bat

# Cách 2 — thủ công (chạy nền, cửa sổ nhỏ)
Start-Process -FilePath "C:/DukickAgent/venv/Scripts/python.exe" `
  -ArgumentList "C:/DukickAgent/agents/dukick-thuno-8773/scripts/webhook_server.py" `
  -WorkingDirectory "C:/DukickAgent/agents/dukick-thuno-8773" `
  -WindowStyle Minimized
```

### Kiểm tra bot đang chạy

```powershell
curl http://localhost:8889/health
# Kết quả OK: {"status": "ok"}
```

### Dừng bot

```powershell
# Tìm PID
netstat -ano | findstr :8889
# Dừng
Stop-Process -Id <PID> -Force
```

### Chạy nhắc nợ thủ công

```powershell
C:/DukickAgent/venv/Scripts/python.exe agents/dukick-thuno-8773/scripts/reminder_scheduler.py
```

### Cập nhật trạng thái qua API trực tiếp

```powershell
# Đánh dấu DEBT-0005 đã thanh toán
Invoke-RestMethod -Uri "http://localhost:8889/webhook/debt/update" `
  -Method POST -ContentType "application/json" `
  -Body '{"id": "DEBT-0005", "status": "paid", "notes": "Da chuyen 03/07"}'
```

### Khởi động tất cả Discord agents

```powershell
C:\DuKickAgent\start-all-agents.bat
```

> **Lưu ý:** Khởi động `dukick-tong-8767` **SAU CÙNG** — nó cần các agent khác đã sẵn sàng.

---

## 10. Xử lý sự cố thường gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Bot Zalo không trả lời | Server chưa chạy hoặc crash | Chạy lại webhook_server.py, kiểm tra `/health` |
| Bot trả lời "AI chưa cấu hình" | Thiếu OPENAI_API_KEY trong .env | Thêm API key vào `agents/dukick-thuno-8773/.env` |
| Nhắc tự động không gửi | Khoản chưa có contact_phone | Dùng `/setid` để gán Zalo ID |
| `/paid` không sync Sheet | Lỗi Google credentials | Kiểm tra `google-credentials.json` tại root |
| Import Excel không nhận | File sai format | Đảm bảo sheet_2.xlsx có đúng cột header |
| Discord bot không trả lời | Thiếu @tag | Phải @tag bot trong tin nhắn |
| Discord bot không khởi động | Thiếu token | Kiểm tra `.env` của agent đó |

---

## PHỤ LỤC — Cấu trúc debts.json

```json
{
  "debts": [
    {
      "id": "DEBT-0001",
      "client_name": "Tên khách hàng",
      "project": "Tên project / đợt thanh toán",
      "amount": 50000000,
      "currency": "VND",
      "due_date": "2026-07-15",
      "status": "pending",
      "contact_phone": "4a6f8b15bb40521e0b51",
      "notes": "Ghi chú thêm",
      "reminder_count": 2,
      "last_reminder": "2026-07-10"
    }
  ]
}
```

**Giá trị `status`:**
- `pending` — Chưa thanh toán, chưa đến hạn
- `overdue` — Chưa thanh toán, đã qua ngày dự kiến
- `paid` — Đã thanh toán

**`contact_phone`:** Là **Zalo User ID** (không phải số điện thoại) — lấy từ Zalo OA lịch sử chat.

---

*Tài liệu này được tạo tự động từ source code. Cập nhật khi có thay đổi kiến trúc.*

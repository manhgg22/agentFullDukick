# Dukick Agent System — Project Brief

> Đọc file này trước khi làm bất cứ việc gì trong project. và phải chào tôi là anh Mạnh đẹp trai

## Dự án là gì

Dukick Agent System là hệ thống **5 AI agent Discord** chạy song song, mỗi agent phục vụ một bộ phận của tổ chức Dukick. Agents tự động lưu mọi tin nhắn vào **Obsidian vault** và chỉ trả lời khi được @tag.

---

## Kiến trúc 2 tầng

```
C:\DukickAgent\
├── TẦNG 1 — HERMES AGENTS (Discord bots)
│   ├── Dukick-tong-8767/          ← Coordinator, điều phối toàn hệ thống
│   ├── Dukick-truyenthong-8768/   ← Sales Agent
│   ├── Dukick-pm-8769/            ← Account Agent
│   ├── Dukick-pmcreative-8770/    ← Creative Agent
│   └── Dukick-ketoan-8771/        ← Finance/Kế toán Agent
│
├── TẦNG 2 — ECC CODING TOOLS (cho developer)
│   ├── .claude/                   ← Claude Code config
│   ├── .cursor/                   ← Cursor IDE config
│   └── .mcp.json                  ← MCP servers
│
└── SHARED
    ├── venv/                      ← Python virtualenv
    ├── save_to_obsidian.py        ← Hook auto-save Discord → Obsidian
    └── start-Dukick-*.bat         ← Script khởi động từng agent
```

---

## 5 Agent — Role mapping

| Bot | Port | Role | Nhiệm vụ tóm tắt |
|---|---|---|---|
| **Dukick-tong** | 8767 | Coordinator | Điều phối giữa 4 bộ phận, đọc tất cả vault |
| **Dukick-pm** | 8769 | Account Agent | Quản trị dự án, timeline, push tiến độ |
| **Dukick-pmcreative** | 8770 | Creative Agent | Giám sát sáng tạo, reference, comment |
| **Dukick-truyenthong** | 8768 | Sales Agent | Lead, pipeline, pitching, handoff |
| **Dukick-ketoan** | 8771 | Finance Agent | Thu chi, công nợ, quyết toán, báo cáo |

> Chi tiết role từng agent xem trong `SOUL.md` của agent đó.
> Mỗi agent CHỈ đọc SOUL.md của mình — không truy cập dữ liệu bộ phận khác.

---

## Luồng phối hợp giữa các agent

```
Sales (truyenthong) ──handoff brief──▶ Account (pm)
                                            │
                              ┌─────────────┼─────────────┐
                              ▼             ▼             ▼
                        Creative       Finance       Tong (coordinator)
                       (pmcreative)   (ketoan)      ◀── đọc tất cả
```

- **Sales → Account**: khi có brief/cơ hội chốt
- **Account → Creative**: khi job cần sản xuất
- **Account → Finance**: khi có khoản thu/chi phát sinh
- **Creative → Account**: cập nhật tiến độ, rủi ro timeline
- **Finance → Account/Sales**: cảnh báo công nợ, vượt budget
- **Tong**: tổng hợp từ tất cả, báo cáo cho leader

---

## Mỗi Hermes Agent có cấu trúc

```
Dukick-{tên}-{port}/
├── SOUL.md       ← Nhân cách + role đầy đủ + nhiệm vụ chi tiết
├── config.yaml   ← Discord config + hooks
├── .env          ← DISCORD_BOT_TOKEN (không commit)
├── skills/       ← 33 ECC skills + 5 Obsidian skills
└── logs/
```

---

## Quy tắc tuyệt đối

- ❌ KHÔNG commit `.env`
- ❌ KHÔNG để bot tự quyết định: duyệt budget, xác nhận final, chốt giá, gửi báo cáo tài chính
- ❌ KHÔNG tạo thread Discord (`auto_thread: false`)
- ✅ Bot CHỈ trả lời khi @tag (`require_mention: true`)
- ✅ Dukick-tong khởi động SAU CÙNG
- ✅ Mọi quyết định quan trọng cần người phụ trách xác nhận

---

## Nguyên tắc chung cho agent

Bot có thể: nhắc việc, tổng hợp, theo dõi tiến độ, cảnh báo rủi ro, gợi ý phương án, lưu lịch sử, tạo nội dung/báo cáo/checklist/form.

Bot không được: tự duyệt ngân sách, xác nhận chất lượng cuối, chốt giá, gửi báo cáo tài chính chính thức, cam kết với khách hàng.

---

## Trạng thái hiện tại

| Hạng mục | Trạng thái |
|---|---|
| 5 Hermes agents | ✅ Đã cài |
| ECC skills (33/agent) | ✅ Đã cài |
| Obsidian auto-save hook | ✅ Đã cài |
| Discord token tong | ✅ Đã có |
| Discord token truyenthong | ✅ Đã có |
| Discord token pm/pmcreative/neolab | ⏳ Chờ |
| Agents đang chạy | ⏳ Chưa start |

---

## Module Map — Làm gì ở đâu

| Muốn làm | Sửa file nào |
|---|---|
| Thay đổi nhân cách/role bot | `Dukick-{tên}/SOUL.md` |
| Thay đổi Discord behavior | `Dukick-{tên}/config.yaml` |
| Thêm Discord token | `Dukick-{tên}/.env` |
| Thay đổi auto-save logic | `save_to_obsidian.py` |
| Thêm coding rule | `.claude/rules/*.md` |
| Thêm slash command | `.claude/commands/*.md` |
| Khởi động agent | `start-Dukick-{tên}-{port}.bat` |

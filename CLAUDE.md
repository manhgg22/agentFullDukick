# DuKick Agent System — Project Brief

> Đọc file này trước khi làm bất cứ việc gì trong project.

## Dự án là gì

DuKick Agent System là hệ thống **5 AI agent Discord** chạy song song, mỗi agent phục vụ một bộ phận của tổ chức DuKick. Agents tự động lưu mọi tin nhắn vào **Obsidian vault** và chỉ trả lời khi được @tag.

---

## Kiến trúc 2 tầng

```
C:\DuKickAgent\
├── TẦNG 1 — HERMES AGENTS (Discord bots)
│   ├── dukick-tong-8767/          ← Coordinator, đọc TẤT CẢ vault
│   ├── dukick-truyenthong-8768/   ← Truyền thông
│   ├── dukick-pm-8769/            ← Project Management
│   ├── dukick-pmcreative-8770/    ← PM Creative
│   └── dukick-neolab-8771/        ← NeoLab
│
├── TẦNG 2 — ECC CODING TOOLS (cho developer)
│   ├── .claude/                   ← Claude Code config
│   ├── .cursor/                   ← Cursor IDE config
│   └── .mcp.json                  ← MCP servers
│
└── SHARED
    ├── venv/                      ← Python virtualenv cho tất cả agents
    ├── save_to_obsidian.py        ← Hook script auto-save Discord → Obsidian
    └── start-dukick-*.bat         ← Script khởi động từng agent
```

---

## Mỗi Hermes Agent có cấu trúc

```
dukick-{tên}-{port}/
├── SOUL.md              ← Nhân cách + role + vault paths
├── config.yaml          ← Discord config + hooks
├── .env                 ← DISCORD_BOT_TOKEN (không commit)
├── skills/              ← 33 ECC skills + 5 Obsidian skills
├── vault-{tên}/         ← Obsidian vault riêng (backup)
└── logs/                ← Runtime logs
```

---

## Module Map — Làm gì ở đâu

| Muốn làm | Sửa file nào |
|---|---|
| Thay đổi nhân cách bot | `dukick-{tên}/SOUL.md` |
| Thay đổi Discord behavior | `dukick-{tên}/config.yaml` |
| Thêm Discord token | `dukick-{tên}/.env` |
| Thay đổi auto-save logic | `save_to_obsidian.py` |
| Thêm coding rule | `.claude/rules/*.md` |
| Thêm slash command | `.claude/commands/*.md` |
| Thêm skill cho agents | `dukick-{tên}/skills/{tên-skill}/SKILL.md` |
| Khởi động agent | `start-dukick-{tên}-{port}.bat` |

---

## Obsidian Vault (Bộ nhớ dài hạn)

```
C:\Users\Admin\Documents\Obsidian Vault\
├── DuKick-Tong/Discord/         ← log tin nhắn kênh tong
├── DuKick-TruyenThong/Discord/  ← log tin nhắn kênh truyenthong
├── DuKick-PM/Discord/           ← log tin nhắn kênh pm
├── DuKick-PMCreative/Discord/   ← log tin nhắn kênh pmcreative
└── DuKick-NeoLab/Discord/       ← log tin nhắn kênh neolab
```

Format: `YYYY-MM-DD.md`, mỗi entry: `### HH:MM — @Username\n{nội dung}`

---

## Quy tắc tuyệt đối

- ❌ KHÔNG commit `.env` (chứa Discord token)
- ❌ KHÔNG trộn config Hermes với ECC
- ❌ KHÔNG tạo thread Discord (`auto_thread: false`)
- ✅ Bot CHỈ trả lời khi bị @tag (`require_mention: true`)
- ✅ dukick-tong khởi động SAU CÙNG (vì là coordinator)
- ✅ Luôn dùng `encoding="utf-8"` trong Python

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

## Phát triển theo Module

Mỗi agent là một module độc lập. Khi làm việc với một agent:
1. Đọc `SOUL.md` của agent đó để hiểu role
2. Đọc `config.yaml` để hiểu behavior
3. Không ảnh hưởng sang agent khác trừ khi có yêu cầu rõ ràng

Khi thêm feature cross-agent: sửa `save_to_obsidian.py` (shared) hoặc cập nhật tất cả `SOUL.md` cùng lúc.

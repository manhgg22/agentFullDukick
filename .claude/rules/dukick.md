---
description: "Dukick project rules — Hermes agents, Discord bots, Obsidian vault"
alwaysApply: true
---

# Dukick Project Rules

## Kiến trúc hệ thống

Project gồm 2 tầng riêng biệt — KHÔNG trộn lẫn config của 2 tầng:

| Tầng | Thư mục | Mục đích |
|---|---|---|
| **Hermes agents** | `Dukick-*/` | Discord bots, chạy qua `hermes_cli` |
| **ECC coding** | `.claude/`, `.cursor/` | Trợ lý code cho developer |

## 5 Hermes Agents

| Agent | Port | Vai trò | Vault |
|---|---|---|---|
| `Dukick-tong-8767` | 8767 | Coordinator — đọc TẤT CẢ vault | `Dukick-Tong` |
| `Dukick-truyenthong-8768` | 8768 | Truyền thông | `Dukick-TruyenThong` |
| `Dukick-pm-8769` | 8769 | Project Management | `Dukick-PM` |
| `Dukick-pmcreative-8770` | 8770 | PM Creative | `Dukick-PMCreative` |
| `Dukick-neolab-8771` | 8771 | NeoLab | `Dukick-NeoLab` |

## Quy tắc khi sửa agent

- Mỗi agent có `SOUL.md` (nhân cách), `config.yaml` (hooks/Discord), `.env` (secrets)
- KHÔNG commit `.env` — chứa Discord bot token
- Khi sửa SOUL.md của một agent, KHÔNG copy sang agent khác (mỗi agent có vai trò riêng)
- Vault path: `C:\Users\Admin\Documents\Obsidian Vault\Dukick-{TenAgent}\`

## Discord bot rules

- `require_mention: true` — chỉ trả lời khi bị @tag
- `auto_thread: false` — KHÔNG tạo thread mới
- Hook `pre_gateway_dispatch` → `save_to_obsidian.py` — tự động lưu mọi tin nhắn

## Python style (Hermes codebase)

- Dùng `venv` tại `C:\DukickAgent\venv\`
- Python executable: `C:/DukickAgent/venv/Scripts/python.exe`
- Encoding: luôn dùng `utf-8` khi đọc/ghi file
- Hermes config: `YAML` format trong `config.yaml`

## Git workflow

- Remote: `https://github.com/manhgg22/agentFullDukick` (private)
- Branch chính: `main`
- KHÔNG commit: `*.db`, `*.pid`, `*.lock`, `*/sessions/`, `*/.env`
- Commit message: `conventional` — `feat:`, `fix:`, `chore:`

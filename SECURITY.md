# Dukick Agent System — Security & Permission Guide

> Tài liệu này mô tả toàn bộ cơ chế bảo mật, phân quyền, và quy trình vận hành an toàn cho hệ thống 6 Hermes Agent Discord của Dukick.

---

## 1. Tổng quan kiến trúc bảo mật

```
Discord User
    │  @mention only
    ▼
Hermes Gateway (per agent)
    │  require_mention: true
    │  auto_thread: false
    ▼
Shell Hook Allowlist  ──►  save_to_obsidian.py
    │  whitelist command
    ▼
Obsidian Vault (local filesystem)
    │  C:\Users\Admin\Documents\Obsidian Vault\
    ▼
Tailscale Funnel (HTTPS public)
    https://admin-pc-1.tailc0eb7b.ts.net/
```

**Nguyên tắc cốt lõi:**
- Bot chỉ phản hồi khi bị @mention — không lắng nghe passive
- Mọi secret nằm trong `.env` local — không commit git
- Shell command chỉ chạy nếu có trong whitelist được approve thủ công
- Vault read/write qua Python only — không dùng shell redirection

---

## 2. Danh sách 6 Agent & Phân quyền

| Agent | Port | Vault | Discord Toolsets | Ghi vault |
|---|---|---|---|---|
| `dukick-tong-8767` | 8767 | `Dukick-Tong` | browser, web, code_execution | Dukick-Tong + đọc tất cả |
| `dukick-truyenthong-8768` | 8768 | `Dukick-TruyenThong` | browser, web, code_execution | Dukick-TruyenThong only |
| `dukick-pm-8769` | 8769 | `Dukick-PM` | browser, web, code_execution | Dukick-PM only |
| `dukick-pmcreative-8770` | 8770 | `Dukick-PMCreative` | browser, web, code_execution | Dukick-PMCreative only |
| `dukick-ketoan-8771` | 8771 | `Dukick-NeoLab` | browser, web, code_execution | Dukick-NeoLab only |
| `hermes-hr-8772` | 8772 | `Dukick-HR` | ❌ none | Dukick-HR only |

> `hermes-hr-8772` bị tắt toolsets intentionally — HR agent không cần browse web hay execute code.

---

## 3. Discord-level Security

### 3.1 Bot Response Gate
Tất cả 6 agent đều có:
```yaml
discord:
  require_mention: true        # chỉ trả lời khi @bot
  auto_thread: false           # không tự tạo thread
  thread_require_mention: true # trong thread cũng phải @mention
```

**Không ai có thể trigger bot bằng cách chat bình thường** — phải @tag trực tiếp.

### 3.2 Phân quyền người dùng Discord
Hiện tại: **không có user-level restriction** — bất kỳ ai trong server có thể @tag bot.

**Recommended (chưa implement):**
```yaml
# config.yaml
discord:
  allowed_roles: ["Manager", "CEO", "Admin"]   # role-based
  allowed_users: ["USER_ID_1", "USER_ID_2"]    # user-based whitelist
```

### 3.3 Hành động bot KHÔNG được phép (enforced trong SOUL.md)
- ❌ Tự duyệt ngân sách hoặc chi phí
- ❌ Xác nhận chất lượng final của sản phẩm
- ❌ Chốt giá với khách hàng
- ❌ Gửi báo cáo tài chính chính thức
- ❌ Cam kết timeline với client
- ❌ Tạo thread Discord mới

---

## 4. Shell Hook Security

### 4.1 Allowlist mechanism
Mỗi agent có file `shell-hooks-allowlist.json` — chỉ command trong này mới được execute:

```json
{
  "approvals": [
    {
      "approved_at": "2026-06-11T04:05:31Z",
      "command": "C:/DukickAgent/venv/Scripts/python.exe C:/DukickAgent/save_to_obsidian.py",
      "event": "pre_gateway_dispatch",
      "script_mtime_at_approval": "2026-06-10T05:10:17Z"
    }
  ]
}
```

**Lưu ý:** `script_mtime_at_approval` — nếu `save_to_obsidian.py` bị sửa sau khi approve, Hermes sẽ từ chối chạy và hỏi lại. **Đây là cơ chế chống tamper.**

### 4.2 Khi cần update save_to_obsidian.py
1. Sửa file
2. Hermes sẽ block hook và hỏi approve lại
3. Approve thủ công từ Discord hoặc terminal
4. `script_mtime_at_approval` tự update

### 4.3 Quy tắc thêm hook mới
- Chỉ thêm command vào `config.yaml` hooks section
- Không hardcode shell command nhạy cảm
- Timeout tối đa 5 giây (tránh blocking gateway)
- Luôn `sys.exit(0)` khi lỗi — không crash bot

---

## 5. Secret Management

### 5.1 File secrets
| File | Nội dung | Commit? |
|---|---|---|
| `agents/*/.env` | `DISCORD_BOT_TOKEN` | ❌ Never |
| `.secrets.env` | API keys dự phòng | ❌ Never |
| `hermes-global.env` | Global Hermes config | ❌ Never |
| `.env.example` | Template không có value | ✅ OK |

### 5.2 .gitignore enforced
```
*/.env
.env
hermes-global.env
.secrets.env
```

### 5.3 API Keys hiện tại
| Provider | Key location | Rotation |
|---|---|---|
| Ollama (kimi-k2.6) | `agents/*/.env` + `config.yaml` fallback | Manual — khi bị 429 rate limit |
| Discord Bot Token | `agents/*/.env` | Manual — qua Discord Developer Portal |

### 5.4 Quy trình rotate key
1. Lấy key mới từ provider
2. Update `agents/*/.env` (từng agent)
3. Update `config.yaml` → `fallback.api_key` nếu có
4. Restart agent: chạy `.bat` tương ứng
5. **Không commit key vào git**

---

## 6. Obsidian Vault Security

### 6.1 Vault write mapping
```
Agent                    →  Vault folder
─────────────────────────────────────────
dukick-tong-8767         →  Dukick-Tong/Discord/
dukick-truyenthong-8768  →  Dukick-TruyenThong/Discord/
dukick-pm-8769           →  Dukick-PM/Discord/
dukick-pmcreative-8770   →  Dukick-PMCreative/Discord/
dukick-ketoan-8771       →  Dukick-NeoLab/Discord/
hermes-hr-8772           →  Dukick-HR/Discord/
```

Mỗi agent **chỉ ghi vào vault của mình** — enforced trong `save_to_obsidian.py` qua `AGENT_VAULT_MAP`.

### 6.2 Public web access
- URL: `https://admin-pc-1.tailc0eb7b.ts.net/`
- Mechanism: Tailscale Funnel → proxy local port 9999 (Quartz static site)
- **Toàn bộ vault được publish public** — không có auth gate

**⚠️ Rủi ro:** Dữ liệu Discord logs, báo cáo nội bộ, tài liệu chiến lược đều visible với internet.

**Recommended:** Thêm Tailscale ACL hoặc basic auth nếu có nội dung nhạy cảm.

### 6.3 Dữ liệu KHÔNG được lưu vault
- Bot token, API key
- Thông tin tài khoản ngân hàng chi tiết
- Password, credential cá nhân
- Thông tin client chưa được phép public

---

## 7. Network & Infrastructure Security

### 7.1 Port exposure
| Port | Service | Access |
|---|---|---|
| 8767–8772 | Hermes agent gateways | Localhost only |
| 9999 | Quartz web server | Localhost → Tailscale Funnel |
| 443 | Tailscale HTTPS | Public internet |

### 7.2 Tailscale
- Funnel: public internet access đến port 9999
- Tailnet only (`:8443`): internal access đến port 4000
- Hostname: `admin-pc-1` trong tailnet `tailc0eb7b.ts.net`

### 7.3 Windows Startup
- **AutoStart task:** `DukickAgents-AutoStart` — chạy `start-all-agents.bat` khi login
- **Watchdog task:** `DukickAgents-Watchdog` — check mỗi 5 phút, restart agent chết
- Cả 2 task chạy với quyền user hiện tại (`Interactive only`)

---

## 8. Incident Response

### 8.1 Bot bị spam / abuse
1. Vào Discord → kick/ban user
2. Bot tự ngừng reply khi user không còn trong server
3. Nếu cần tắt bot ngay: `Stop-Process -Id (Get-Content agents\{name}\gateway.pid | ConvertFrom-Json).pid`

### 8.2 API key bị leak
1. Revoke key ngay tại provider dashboard
2. Generate key mới
3. Update tất cả `.env` files
4. Restart agents
5. Check git log: `git log --all -p | grep -i "api_key\|token"` — verify không commit

### 8.3 Bot token bị compromise
1. Discord Developer Portal → Bot → Regenerate Token
2. Update `agents/{agent}/.env` → `DISCORD_BOT_TOKEN=<new>`
3. Restart agent đó
4. Monitor Discord Audit Log

### 8.4 Agent không tự restart
1. Check watchdog: `Get-ScheduledTask -TaskName "DukickAgents-Watchdog"`
2. Manual trigger: `Start-ScheduledTask -TaskName "DukickAgents-Watchdog"`
3. Check logs: `agents/{name}/logs/`

---

## 9. Checklist Vận hành Định kỳ

### Weekly
- [ ] Check 6 agents alive: `watchdog-agents.ps1` output
- [ ] Review Obsidian vault — xóa nội dung nhạy cảm nếu có
- [ ] Check disk space (vault + git pack có thể lớn nhanh)

### Monthly
- [ ] Rotate Ollama API key nếu gần limit
- [ ] Review `shell-hooks-allowlist.json` — xóa approval cũ không dùng
- [ ] Review Discord bot permissions trên Developer Portal
- [ ] `git log --oneline -20` — verify không có commit chứa secret

### Khi onboard member mới
- [ ] Giải thích rule: chỉ @tag bot khi cần, không chat với bot như người thật
- [ ] Không share bot token với bất kỳ ai
- [ ] Không push `.env` files lên git

---

## 10. Cấu trúc repo liên quan đến security

```
C:\DuKickAgent\
├── agents/*/
│   ├── .env                      ← SECRET — không commit
│   ├── config.yaml               ← require_mention, toolsets, fallback key
│   ├── shell-hooks-allowlist.json ← whitelist shell commands
│   └── SOUL.md                   ← behavioral constraints
├── save_to_obsidian.py           ← hook ghi vault (approved)
├── watchdog-agents.ps1           ← auto-restart
├── .gitignore                    ← excludes .env, secrets
└── SECURITY.md                   ← file này
```

---

*Last updated: 2026-06-24 | Maintainer: anh Mạnh (manhgg22)*

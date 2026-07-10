# Dukick HR Vault Structure

## Vault Path
`C:\Users\Admin\Documents\Obsidian Vault\Dukick-HR\`

## Folder Conventions

| Folder | Purpose |
|--------|---------|
| `TaiLieu-NhanSu/` | Employee lists, contracts, org charts, account lists, salary data, violation records |
| `ChinhSach/` | Policies, regulations, benefit rules, internal regulations, salary schemes |
| `TuyenDung/` | Job descriptions, interview schedules, candidate data, recruitment plans |
| `Onboarding/` | Training materials, onboarding checklists, orientation docs |
| `QuanTri/` | Administrative plans, KPIs, salary structures, HR strategy documents, job descriptions |
| `Discord/` | Auto-saved Discord message logs (if enabled) |

## Active Data Catalog

### As of 2026-06-29

| File | Location | Contents | Confidentiality |
|------|----------|----------|---------------|
| `Danh_sach_tai_khoan_Dukick.csv` | `TaiLieu-NhanSu/` | Company account credentials by department (Gmail, tool accounts, passwords) | 🔴 HIGH — contains plaintext passwords |
| `Danh_sach_nhan_su_T11.2025.csv` | `TaiLieu-NhanSu/` | Employee roster Nov 2025 (CCCD, phone, address, MBTI, work status) | 🔴 HIGH — contains PII |
| `Ke_hoach_HCNS_2026.csv` | `QuanTri/` | 2026 HR administrative plan (6 strategic pillars, monthly timeline) | 🟡 MEDIUM — internal strategy |
| `Dinh_bien_nhan_su_2026.csv` | `TaiLieu-NhanSu/` | Staffing plan Dec 2025 → Jul 2026 (headcount, positions, salaries) | 🔴 HIGH — contains salary data |
| `Mo_ta_cong_viec_Ke_toan_Dukick.csv` | `QuanTri/` | Accountant JD — 8 roles: cash flow, revenue/expense, documents, debt, tax, payroll, insurance, BOD directives | 🟡 MEDIUM — internal process |
| `Co_che_luong_job_AI.csv` | `ChinhSach/` | AI job salary scheme (5 tiers VVIP→A+, AI multiplier L1-L4, lead 2-6M, member 1.3-3.9M) | 🔴 HIGH — salary structure |
| `Co_che_luong_job_PM.csv` | `ChinhSach/` | PM job salary scheme (Hoàng/Thái: 9% net profit; new hire: 8%; Sales 60%/Production 40%; from May 2026) | 🔴 HIGH — salary structure |
| `Vi_pham_noi_quy_nhan_su.csv` | `TaiLieu-NhanSu/` | Employee violation records (12 staff, fines 50k–500k, 3x process violation = termination) | 🟡 MEDIUM — disciplinary data |
| `Che_o_ai_ngo_fulltime_Dukick.csv` | `ChinhSach/` | Full-time benefits 2025 (15 policies: sick leave 300k, maternity 500k, Tet bonus = 13th month, travel, YEP, etc.) | 🟢 LOW — public-facing policy |

## Naming Conventions
- Use snake_case for file names
- Include date/version suffix if multiple versions exist (e.g., `_v2`, `_2026-06`)
- Keep original language in filename (Vietnamese preferred)

## Notes for Future Sessions
- Always check this catalog before writing new files to avoid overwriting.
- If the user asks about "nhân sự", "tài khoản", "lương", or "kế hoạch HCNS", the data is likely already in this vault.
- Salary and credential data must never be echoed in full in chat responses.
- Violation records and disciplinary data are sensitive — summarize patterns, never name individuals unless explicitly asked.

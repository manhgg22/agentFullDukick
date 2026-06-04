---
name: production-proposals
description: >
  Generate client-facing proposal decks, shooting proposals/treatments, and detailed quotations
  for creative/production agencies (TVC, photo, events). Covers brief analysis, slide generation
  via python-pptx, and structured quotation tables (Markdown/CSV). Built around DuKick PM
  workflow but adaptable to any production agency.
---

# production-proposals

## When to use
- User asks to **"phân tích brief"**, **"soạn proposal / shooting proposal / treatment"**, **"làm báo giá / quotation"**, or **"chốt giá"**.
- Any request to create pitch materials, client decks, or pricing documents for a production job.
- Brief sources may be: Canva links, Google Docs links, PDFs, pasted text, or screenshots.

## Workflow

### 1. Brief Intake & Analysis
**Always read/extract the brief first.** Try in this order:
1. **Link-based brief (Canva, Google Docs, etc.):**
   - Attempt `execute_code` + `requests` to fetch HTML and strip text.
   - **Pitfall — Canva share links:** `canva.link/...` and `canva.com/design/.../edit` often return **shell HTML** that requires login. The actual design content is loaded client-side by JS and is not accessible via simple HTTP GET.
   - **Fallback:** Ask user to download as PDF/PNG, copy-paste content, or share screenshots → analyze via `vision_analyze`.
2. **Image/screenshot brief:** Load via `vision_analyze` with questions about brand, product, objective, tone, don'ts.
3. **Copy-pasted text:** Analyze directly.

**Brief analysis checklist (DUKICK/TVC):**
- Thông tin KH & sản phẩm (brand, product, category)
- Insight & mục tiêu truyền thông
- Insight người dùng (nếu có)
- Tone & Mood
- Giới hạn / Don'ts
- Deliverables format yêu cầu
- Timeline mong muốn
- **Rủi ro tiềm ẩn:** brief thay đổi muộn, nhiều tầng duyệt, KH ít chuyên môn nhưng nhiều ý kiến, KH trịnh thượng

> **Nguyên tắc DuKick:** KH đổi brief muộn → thông báo phát sinh chi phí ngay. Mọi bước quan trọng có email/biên bản.

### 2. Proposal Deck (Shooting Proposal / Treatment)
Generate `.pptx` using `python-pptx`.
- If `pptx` missing: `pip install python-pptx` then import.

**Standard slide structure (DuKick Shooting Proposal):**
1. **Cover** — Client name + Project name + "SHOOTING PROPOSAL"
2. **Tổng quan dự án** — Duration, format, insight, objective, delivery date
3. **Creative Direction** — Tone/mood, color palette, pacing, music/SFX, don'ts
4. **Narrative & Storyboard** — 3-act structure (Hook 0–5s / Body 5–25s / CTA 25–30s), shot count, backup shots
5. **Kế hoạch sản xuất** — Pre-prod → On-set → Post
6. **Ekip & Thiết bị** — Crew list + camera/lighting/gimbal/drone
7. **Deliverables** — Master 4K + social cuts + frame grabs + subtitles
8. **Timeline** — Day-by-day schedule (ngày 1–20 mẫu)
9. **Investment / Đầu tư** — Budget intro slide
10. **Báo giá tổng quan** — Scope summary + phát sinh disclaimer

**Technical notes:**
- Import color: `from pptx.dml.color import RGBColor` (must be **RGBColor**, `RgbColor` fails).
- Slide size 16:9: `prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)`.
- Blank layout index: `prs.slide_layouts[6]`.
- Save to Windows path: `C:/DuKickAgent/...` works fine in Python.

### 3. Detailed Quotation (Báo giá)
Provide **both** formats:
- **Markdown** — For Discord / Notion / email body (dễ đọc, dễ sửa).
- **CSV / Excel** — For finance/PMO import.

**Hạng mục chuẩn (Production Agency):**
- **A. Pre-production:** Concept & Creative Direction, Storyboard, PPM
- **B. Production (On-set):** Producer/PM, Đạo diễn, DOP + Camera Assistant, Gaffer + Lighting, Makeup & Hair + Stylist, Location/Studio, Cast/Talent, Catering & Logistics
- **C. Post-production:** Offline Edit, Online (Color Grading + GFX), VFX/CGI (nếu có), Sound Design & Mixing, Voiceover / VO
- **D. Deliverables:** Master 4K + Social cuts (15s/30s/6s) + Frame grabs

**Điều khoản thanh toán mẫu:**
- **Đợt 1:** 30% ký hợp đồng
- **Đợt 2:** 40% sau khi duyệt Offline
- **Đợt 3:** 30% sau khi bàn giao final
- **Phát sinh ngoài scope:** Báo trước bằng văn bản, không tự ý chốt giá.

## Pitfalls
1. **Canva links are login-walled:** Do not spend multiple turns parsing shell HTML. Prompt user for PDF/screenshot immediately after first failed fetch.
2. **python-pptx RGBColor import:** `RgbColor` (lowercase) is wrong — use `RGBColor`.
3. **Scope creep:** Always include a "phát sinh ngoài scope" disclaimer and 3-đợt payment terms.
4. **Windows paths in Python:** Use forward slashes `C:/...` or `/c/...` inside `execute_code`; backslashes need escaping.
5. **Template vs Custom:** If brief content is inaccessible, generate a **template with placeholders** and clearly label it as a skeleton to be filled after receiving the actual brief. Do not fabricate specific brand details.

## Templates & Scripts
- `templates/shooting_proposal_generator.py` — Python script that generates the standard 10-slide DuKick Shooting Proposal deck.
- `templates/quotation_template.md` — Markdown quotation template (suitable for Discord/Notion/email).
- `templates/quotation_template.csv` — CSV quotation template for finance tracking.

## References
- `references/canva_brief_pitfall.md` — Deep dive on why Canva share links fail and recommended workarounds.

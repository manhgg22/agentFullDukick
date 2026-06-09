---
name: dukick-account
description: |
  Quản lý dự án TVC / chụp ảnh / shoot tại DuKick — agency sản xuất video & hình ảnh.
  Hướng dẫn Account/PM từ nhận brief, phân tích nội dung, đánh giá khách hàng,
  benchmark ngân sách, packaging đa tầng, đến soạn proposal/báo giá và quản trị rủi ro
  trong suốt vòng đời dự án.
trigger:
  - User là Account/PM tại DuKick hoặc thảo luận về dự án TVC / chụp ảnh / shoot
  - Cần đánh giá job mới, báo giá, hoặc quyết định go/no-go
  - Xử lý tình huống với khách hàng, freelancer, hoặc nội bộ sản xuất
  - Cần viết meeting minutes, call sheet, offline note, hoặc nghiệm thu
  - Điều phối giữa Creative, Sản xuất, Editor, và Khách hàng
  - User shares a prospective client brief and asks for assessment or recommendation
  - A suspected budget gap exists between client expectation and agency standard pricing
  - Team member requests tactical analysis of a new lead (go/no-go, packaging options)
  - A Google Doc or brief link is inaccessible and needs text extraction
  - User asks to "review" or "analyze" a customer inquiry
  - Yêu cầu phân tích brief, soạn shooting proposal, làm báo giá, chốt giá
---

# DuKick Account — Quản Trị Dự Án Sản Xuất TVC & Hình Ảnh

## I. Tư Duy Cốt Lõi (Mindset)

### Ownership
Account là "Giám đốc điều hành thu nhỏ" của dự án. Không đổ lỗi cho Client "khó tính" hay Ekip "làm ẩu". Mọi kết quả — thành công hay thất bại — Account chịu trách nhiệm cao nhất về vận hành.

### Solution-oriented
Khi báo cáo 1 vấn đề, phải đi kèm ít nhất **2 giải pháp** kèm ưu/nhược điểm để Sếp hoặc Client lựa chọn.

### Client-centric không Servile
Thấu hiểu KH nhưng push-back khi yêu cầu làm tổn hại chất lượng hoặc lợi ích công ty.

---

## II. Kiềng Ba Chân — Quality | Timeline | Budget

| Trụ cột | Nguyên tắc | Hậu quả nếu đổ |
|---------|-----------|----------------|
| **Quality** | Sản phẩm đạt tiêu chuẩn thẩm mỹ + yêu cầu KH | Mất uy tín, không tái ký |
| **Timeline** | Bám sát lịch, trễ 1–2 tháng gây hậu quả lớn cho thương hiệu | Phạt hợp đồng, mối quan hệ xấu |
| **Budget** | Kiểm soát chi phí, hạn chế phát sinh trên set | Lỗ vốn, lãi thấp |

---

## III. Kỹ Năng Cốt Lõi

### 1. Phiên dịch hai chiều (Translator)
- **Client → Nội bộ**: "Làm cho sang lên" → ngôn ngữ kỹ thuật đo lường được (VD: tăng độ phân giải, dùng ống kính tele, grading vintage)
- **Nội bộ → Client**: Khó khăn kỹ thuật → ngôn ngữ kinh doanh đơn giản

### 2. Expectation Management
- **Under-promise, Over-deliver**. Không hứa bừa khi chưa check ekip.
- Lập rõ **Scope of Work** từ đầu: trong ngân sách vs phát sinh.
- Nếu KH đổi brief muộn → thông báo phát sinh chi phí ngay.

### 3. Quản trị rủi ro
- Luôn có **Plan B, Plan C**.
- Quay **backup shots** dự phòng hậu kỳ.
- Nhìn thấy nguy cơ trước khi xảy ra.

### 4. Documentation — Xác nhận bằng văn bản
- Mọi bước quan trọng có email/biên bản: Kịch bản, PPM, Call-sheet, Offline, Nghiệm thu.
- File gửi ra ngoài: **comment only, không cho edit**.

---

## IV. Nhận Brief & Trích Xuất Nội Dung

**Luôn đọc/trích xuất brief trước khi phân tích.** Thử theo thứ tự:

### 1. Link-based brief (Canva, Google Docs)
- **Canva share link:** Thường trả về HTML shell (cần login). Không dùng `requests` để đọc nội dung văn bản. Hành động: yêu cầu KH gửi file PDF/PNG hoặc chụp màn hình từng trang. Xem chi tiết tại `references/canva-brief-pitfall.md`.
- **Google Docs:** Nếu link yêu cầu login, dùng fallback `r.jina.ai` để trích xuất văn bản. Xem chi tiết tại `references/google-doc-extraction.md`.

### 2. File PDF
1. Thử `pdfplumber` để extract text.
2. Nếu `page.extract_text()` trả về rỗng → PDF là image-based (scan/design).
3. **Pipeline image-based PDF** (kỹ thuật then chốt): dùng PyMuPDF chuyển từng trang thành PNG, sau đó nối thành batch (4–5 trang/batch) để `vision_analyze` đọc. Xem chi tiết tại `references/pdf-image-extraction-pipeline.md`.

### 3. File ảnh / Screenshot
- Dùng `vision_analyze` trực tiếp.
- Nếu nhiều ảnh → nối thành strip dọc bằng PIL.

---

## V. Cấu Trúc Phân Tích Brief

Phân tích theo 10 mục chuẩn — dùng markdown table/bullet để rõ ràng:

| Mục | Ý nghĩa |
|-----|---------|
| **Tổng quan dự án** | Tên dự án, KH, loại hình, concept, số scene |
| **Scene-by-scene** | Mỗi scene: Key Mood, Hero Shot, Shot list (Wide/Medium/Close-up/Motion), Ánh sáng, Địa điểm, Props |
| **Casting** | Số lượng, độ tuổi, vai vế, giới hạn giờ (đặc biệt trẻ em) |
| **Wardrobe** | Số set, tone màu, phong cách |
| **Yêu cầu kỹ thuật** | Tỷ lệ khung hình, ánh sáng, camera movement, định dạng đầu ra |
| **Deliverables** | Số ảnh, số video, độ phân giải, format file |
| **Timeline** | Ngày quay, ngày bàn giao, số ngày dự kiến |
| **Ngân sách** | Có báo giá từ KH không? Nếu không → DuKick cần báo giá riêng |
| **Usage Rights** | Thời hạn, lĩnh vực, exclusive/non-exclusive |
| **Contact & Quy trình duyệt** | Ai duyệt final? Có agency thứ 3 không? |

### Đánh giá điểm mạnh / yếu của brief

**Điểm mạnh thường gặp:**
- Có mood board, reference ảnh
- Shot list phân loại rõ (Wide/Medium/Close-up/Motion)
- Props list đầy đủ
- Reference camera movement / link YouTube

**Điểm yếu / Thiếu sót cần hỏi lại:**
- Không có báo giá → DuKick cần báo giá riêng
- Không có lịch trình chi tiết (call-sheet, phân ca)
- Không có định dạng đầu ra cụ thể (bao nhiêu ảnh? 4K/1080p?)
- Không có usage rights
- Ngày quay không hợp lý / đã quá hạn
- Không ghi rõ số ngày quay
- Không có contact person / quy trình duyệt

---

## VI. Prospect Company Research & Budget Benchmarking

### 1. Nội bộ — Khai thác dữ liệu lịch sử
- Đọc vault / Discord logs / project notes về tương tác trước với KH hoặc KH tương tự.
- Tìm anchor giá bằng regex: `'\\b\\d+M\\b'`, `budget`, `triệu`, `gói` trong markdown logs.
- Cite log filenames, dates, hoặc tên job cũ để làm bằng chứng.

### 2. Ngoại bộ — Nghiên cứu công ty KH
- Scrape website KH: industry, size, leadership, positioning, B2B vs B2C.
- Đánh giá độ chuyên nghiệp sản xuất: đã từng làm video chuyên nghiệp chưa?
  (KH B2B niche thường đánh giá thấp chi phí 5–10x.)

### 3. So sánh ngân sách
- So sánh với: (a) agency floor / pricing tiers, (b) internal comparable jobs, (c) market norms.
- Định lượng chênh lệch (gap). Cảnh báo "budget shock" khi gap ~>3x.

---

## VII. Duyệt Sơ Bộ — Go / Adjust / No-Go

Trước khi packaging báo giá, chạy fast triage theo 4 yếu tố:

| Factor | Red Flag | Impact |
|--------|----------|--------|
| **Budget gap** | Agency floor >25% above client expectation | Win rate drops sharply |
| **Selection criteria** | Client chọn **chỉ theo giá** (không chấm treatment/quality) | Higher price almost always loses |
| **Relationship** | Không có prior work hoặc warm intro | Không trust premium để offset giá |
| **Opportunity cost** | Team capacity chật hoặc có lead tiềm năng hơn | Thời gian ở đây = mất win ở chỗ khác |

**Decision matrix:**
- **0–1 red flags** → Tiếp tục packaging đa tầng (Step VIII).
- **2 red flags** → Cân nhắc single-option slimmed-down hoặc touchpoint quan hệ.
- **3–4 red flags** → **Polite decline.** Không đốt giờ làm proposal near-zero-win.

**Mẫu từ chối lịch sự:**
> "Em cảm ơn anh/chị đã cân nhắc DuKick. Sau khi đánh giá khối lượng công việc và so sánh với ngân sách dự kiến, em nhận thấy với mức đầu tư hiện tại, chúng em không đảm bảo được chất lượng đầu ra theo tiêu chuẩn của mình. Rất tiếc lần này chưa phù hợp để hợp tác. Mong có cơ hội khác ạ."

---

## VIII. Packaging Đa Tầng (Multi-tier Options)

**Bắt buộc khi gap >3x và vẫn tiếp tục.**

Thiết kế pricing ladder:
- **Tier 1 (Fit budget):** Minimal viable scope; nêu rõ giới hạn.
- **Tier 2 (Mid):** Selective quality upgrades (camera tốt hơn, thêm voice-over, v.v.).
- **Tier 3 (Premium):** Full-scope standard production đúng positioning agency.

Mỗi tier ghi rõ: scope, timeline, exclusions.

---

## IX. Soạn Proposal & Báo Giá

### 1. Proposal Deck (.pptx)
Sử dụng `python-pptx` để tạo slide. Nếu thiếu: `pip install python-pptx`.

**Cấu trúc slide chuẩn DuKick Shooting Proposal (10 slide):**
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
- Import color: `from pptx.dml.color import RGBColor` (**RGBColor**, không phải `RgbColor`)
- Slide size 16:9: `prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)`
- Blank layout index: `prs.slide_layouts[6]`
- Template script có sẵn: `templates/shooting_proposal_generator.py`

### 2. Detailed Quotation (Báo giá)
Cung cấp **cả hai** format:
- **Markdown** — For Discord / Notion / email body.
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

---

## X. Quy Trình TVC Tại DuKick

### Tiền kỳ (Pre-production)
1. Brief đầy đủ → Concept / Storyline
2. **PPM** — chốt Treatment, Storyboard, kế hoạch quay
3. Nếu KH đổi brief muộn → thông báo phát sinh chi phí ngay

### On-set
- Phiên dịch Đạo diễn ↔ Khách
- Kiểm soát **OT** (chi phí OT rất đắt)
- Quay **backup shots** (cảnh cận dự phòng)
- **Lấy chữ ký xác nhận shot cuối ngày**
- TVC: tối đa **25 shots/ngày quay**

### Hậu kỳ (Post-production)
- Phân biệt **Offline** (nhịp/nhạc/line) vs **Online** (màu/VFX) cho khách
- **Feedback Filter**: lọc comment hợp lý → Editor | vô lý → giải thích cho KH
- Dịch ngôn ngữ KH → ngôn ngữ kỹ thuật cho Editor

---

## XI. Daily Routine — 3 Vòng Kiểm Soát

### Vòng 1: Khách hàng (External)
- Chủ động update tiến độ — đừng để KH phải hỏi
- Trả lời trong vòng **15 phút** (nếu bận: báo phản hồi sau 1–2 tiếng)
- Gửi **meeting minutes** sau mỗi cuộc họp
- Luôn chuyên nghiệp, từ tốn → Bán hàng tư vấn

### Vòng 2: Nội bộ (Internal)
- Check tiến độ Creative, Sản xuất, Editor
- Nhắc việc trong group: đánh **STT**, tag người phụ trách, **deadline bold**
- Truyền đạt feedback chuẩn xác, không bộp chộp

### Vòng 3: Tài chính (Admin)
- Theo dõi thanh toán **3 đợt**
- Đôn đốc KH thanh toán đúng hạn
- Kiểm soát phát sinh

---

## XII. Quy Ước Đặt Tên & Tổ Chức

- **Group KH**: `Client [Brand] - Dukick`
- **Group nội bộ**: `DKnb [Level].[Tên job tối giản].[Ngày onset]`
- **Folder job**: `[Tình hình] [Level].[Tên job]`

---

## XIII. Nguyên Tắc Bất Biến

- **Không tự duyệt budget, xác nhận final, chốt giá hay cam kết với khách khi chưa có xác nhận.**
- Luôn hỏi lại khi thiếu dữ liệu.
- Mọi thay đổi quan trọng phải lưu: **ai, lúc nào, thay đổi gì, lý do**.
- KH đổi brief muộn → thông báo phát sinh chi phí ngay. Mọi bước quan trọng có email/biên bản.
- Scope of Work ký từ đầu; thay đổi sau ký = phụ phí.
- Under-promise, over-deliver.

---

## XIV. Case Studies Thực Tế

### Hanoi Signature — Nhiều tầng duyệt, brief thay đổi liên tục
→ Chốt định hướng bằng văn bản sau mỗi lần KH duyệt.
→ Quay cảnh cận dự phòng dù KH yêu cầu cảnh toàn.
→ Cân bằng nghệ thuật (Đạo diễn) vs hiệu quả kinh doanh (KH).

### May 10 — KH + Agency không chuyên nhưng hay ý kiến
→ Đơn giản hóa ý tưởng, loại bỏ ẩn dụ phức tạp.
→ Ghi số giây từng cảnh trong Storyboard để KH hình dung nhịp phim.
→ Editor on-set: dựng phim ngay tại hiện trường.
→ Pick-up shots theo ý đồ nghệ thuật đảm bảo chất lượng tối thiểu.

### HATECO — KH trịnh thượng, ít chuyên môn
→ Công thức 80/20: đồng ý 80% ý kiến KH → tạo tin tưởng → dùng 20% tư vấn chỉ ra rủi ro.
→ Để KH tự nhận ra vấn đề qua tư vấn, không khẳng định mình đúng ngay.

---

## XV. Action Items Cho Account (Sau Phân Tích Brief)

1. Gửi email KH xác nhận ngày quay + câu hỏi cần làm rõ
2. Chuẩn bị báo giá sơ bộ (2 phương án)
3. Book recce location (trước 1 tuần)
4. Casting call (trước 7–10 ngày)
5. Styling meeting (chốt set đồ)
6. Chuẩn bị call-sheet mẫu
7. Kiểm tra permit / xin phép location

---

## XVI. Pitfalls

1.  **Chấp nhận job giá thấp để "có việc"** → Lỗ vốn, ảnh hưởng brand positioning.
2.  **Không lọc feedback KH** → Editor bị overload, chất lượng giảm.
3.  **Quên lấy chữ ký xác nhận shot cuối ngày** → KH đổi ý hậu kỳ, phát sinh chi phí.
4.  **Không kiểm soát OT** → Chi phí vượt ngân sách đáng kể.
5.  **Gửi file cho KH ở dạng editable** → KH tự sửa, mất kiểm soát version.
6.  **Brief freelancer lộ tên KH/brand** → Vi phạm bảo mật.
7.  **Không báo phát sinh ngay khi KH đổi scope** → Sau này đòi tiền khó khăn.
8.  **Locked brief documents** — Đừng bỏ brief chỉ vì Google Docs yêu cầu login. Dùng jina.ai fallback.
9.  **Scraping JS-heavy sites** — HTML chỉ cần regex; không render JavaScript.
10. **Single-option rejection** — Không trả lời chỉ 1 giá cao khi KH ngân sách thấp. Luôn đưa ladder (trừ khi triage rõ no-go).
11. **Assuming client sophistication** — KH B2B niche thường không hiểu sản xuất; giải thích tier bằng ngôn ngữ business, không jargon kỹ thuật.
12. **Canva links are login-walled** — Đừng lãng phí nhiều lượt parse shell HTML.
13. **python-pptx RGBColor import** — Dùng `RGBColor` (hoa), không phải `RgbColor` (thường).
14. **Scope creep** — Luôn có disclaimer "phát sinh ngoài scope" và điều khoản 3 đợt thanh toán.
15. **Price-only competitions with a large gap** — Khi KH chọn chỉ theo giá và floor >25% trên market band, EV của proposal thấp gần 0. Polite decline giữ team capacity và brand positioning.
16. **Missing internal benchmarks** — Proposal không anchor cảm thấy tùy tiện, giảm credibility Account.
17. **Not asking for PDF/screenshot when links fail** — Brief analysis blocked by uncooperative formats; always pivot to alternative extraction quickly.

---

## XVII. Evaluation Checklist

- [ ] Brief đầy đủ, đã chốt Scope of Work
- [ ] Duyệt sơ bộ go/no-go đã hoàn thành
- [ ] Vault/ngoại bộ đã scan cho client history và budget anchors
- [ ] Brief đã trích xuất đầy đủ (link/PDF/ảnh) với tất cả trường bắt buộc
- [ ] Budget gap đã định lượng với bằng chứng nội bộ
- [ ] Ít nhất 2 pricing tiers đã đề xuất khi gap đáng kể
- [ ] PPM / Treatment / Storyboard đã duyệt
- [ ] Call-sheet đã gửi, chữ ký xác nhận shot cuối ngày
- [ ] Backup shots đã quay đủ
- [ ] Offline đã duyệt trước khi Online
- [ ] Feedback đã lọc, truyền đạt chuẩn xác cho Editor
- [ ] Meeting minutes đã gửi trong vòng 2 tiếng
- [ ] Thanh toán 3 đợt đang đúng tiến độ
- [ ] File gửi KH ở chế độ comment-only
- [ ] Proposal/báo giá đã bao gồm disclaimer phát sinh + timeline rõ ràng

---

## References
- `references/case-studies.md` — Chi tiết các case HNS, May 10, Hateco
- `references/pricing-benchmarks.md` — Ngưỡng giá chuẩn cho TVC, chụp ảnh, video ngắn
- `references/client-templates.md` — Template email, meeting minutes, từ chối lịch sự, nghiệm thu
- `references/google-doc-extraction.md` — Fallback trích xuất Google Docs yêu cầu login
- `references/pdf-image-extraction-pipeline.md` — Pipeline trích xuất nội dung từ PDF image-based (designer/scan PDFs)
- `references/canva-brief-pitfall.md` — Chi tiết vì sao Canva share links thất bại và workarounds

## Templates & Scripts
- `templates/shooting_proposal_generator.py` — Python script sinh deck .pptx 10 slide chuẩn DuKick

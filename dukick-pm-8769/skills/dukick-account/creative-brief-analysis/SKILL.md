---
title: Creative Brief Analysis for TVC & Photo Shooting
name: creative-brief-analysis
description: Quy trình phân tích brief sản xuất TVC / chụp ảnh / shooting proposal từ KH, và chuẩn bị tài liệu đối ứng (shooting proposal + báo giá) cho DuKick Production.
version: 1.0
triggers:
  - "phân tích brief"
  - "review brief"
  - "shooting proposal"
  - "báo giá chụp ảnh"
  - "báo giá TVC"
  - "đọc brief từ link"
  - "phân tích production brief"
  - "soạn proposal quay phim"
dependencies: []
---

# Creative Brief Analysis — Account Agent Workflow

Skill này hướng dẫn quy trình phân tích brief sản xuất TVC / chụp ảnh lifestyle / shooting proposal từ KH, và chuẩn bị tài liệu đối ứng (shooting proposal + báo giá) cho DuKick.

## 1. NHẬN BRIEF TỪ KH

### 1.1 Canva / Link ngoài
- **Canva share link**: Thường trả về HTML shell (cần login). Không dùng `curl` hay `requests` để đọc nội dung văn bản.
- **Hành động**: Ngay lập tức yêu cầu KH gửi file PDF/PNG hoặc chụp màn hình từng trang.

### 1.2 File PDF
1. Thử `pdfplumber` để extract text.
2. Nếu `page.extract_text()` trả về rỗng → PDF là image-based (scan/design).
3. **Pipeline image-based PDF** (kỹ thuật then chốt):
   ```python
   import fitz  # PyMuPDF
   doc = fitz.open(pdf_path)
   for i, page in enumerate(doc):
       pix = page.get_pixmap(dpi=200)
       pix.save(f"page_{i+1:02d}.png")
   ```
4. Nối các ảnh thành batch (4–5 trang/batch) để `vision_analyze` đọc.
5. Lưu ý giới hạn context — nên đọc từng batch và tổng hợp sau.

### 1.3 File ảnh / Screenshot
- Dùng `vision_analyze` trực tiếp.
- Nếu nhiều ảnh → nối thành strip dọc bằng PIL.

## 2. CẤU TRÚC PHÂN TÍCH BRIEF

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

## 3. ĐÁNH GIÁ ĐIỂM MẠNH / YẾU CỦA BRIEF

### ✅ Điểm mạnh thường gặp
- Có mood board, reference ảnh
- Shot list phân loại rõ (Wide/Medium/Close-up/Motion)
- Props list đầy đủ
- Reference camera movement / link YouTube

### ⚠️ Điểm yếu / Thiếu sót cần hỏi lại
- Không có báo giá → DuKick cần báo giá riêng
- Không có lịch trình chi tiết (call-sheet, phân ca)
- Không có định dạng đầu ra cụ thể (bao nhiêu ảnh? 4K/1080p?)
- Không có usage rights
- Ngày quay không hợp lý / đã quá hạn
- Không ghi rõ số ngày quay
- Không có contact person / quy trình duyệt

## 4. RỦI RO TIỀM ẨN — BACKUP PLAN

| Rủi ro | Mức độ | Backup |
|--------|--------|--------|
| Thời tiết xấu | Cao | Pick-up day; chuyển indoor trước |
| Trẻ em không hợp tác | TB | Bảo mẫu on-set; quay trẻ nhỏ trước, trẻ lớn sau |
| Location chưa sẵn sàng | TB | Recce 1 tuần trước; xác nhận văn bản |
| Golden hour ngắn | Cao | Pre-light 30 phút; sẵn sàng quay ngay khi có ánh sáng |
| Casting không đạt | TB | Casting trước 7–10 ngày; 2 options/vai |
| KH đổi brief | Cao | SOW ký từ đầu; mọi thay đổi email xác nhận + phụ phí |

## 5. ĐỀ XUẤT PHƯƠNG ÁN SẢN XUẤT

Luôn đưa ra **ít nhất 2 phương án** với ưu/nhược điểm:

- **Phương án A (rút gọn)**: 1 ngày — tiết kiệm nhưng rủi ro cao
- **Phương án B (khuyến nghị)**: 2 ngày — đảm bảo chất lượng, có backup shots

## 6. TÀI LIỆU ĐỐI ỨNG

Khi KH cần shooting proposal + báo giá, dùng template sẵn:
- `references/shooting_proposal_template.pptx` — 11 slide chuẩn DuKick
- `references/bao_gia_template.md` — Báo giá markdown (dễ copy lên Notion/Discord)
- `references/bao_gia_template.csv` — Báo giá spreadsheet

## 7. ACTION ITEMS CHO ACCOUNT

Sau khi phân tích xong, luôn liệt kê checklist cụ thể:
1. Gửi email KH xác nhận ngày quay + câu hỏi cần làm rõ
2. Chuẩn bị báo giá sơ bộ (2 phương án)
3. Book recce location (trước 1 tuần)
4. Casting call (trước 7–10 ngày)
5. Styling meeting (chốt set đồ)
6. Chuẩn bị call-sheet mẫu
7. Kiểm tra permit / xin phép location

## 8. NGUYÊN TẮC BẤT BIẾN

- Không báo giá ngay khi brief thiếu thông tin vận hành.
- Mọi thỏa thuận quan trọng phải có văn bản (email xác nhận).
- Ngày quay, deliverables, usage rights → phải chốt trước khi ký hợp đồng.
- Scope of Work ký từ đầu; thay đổi sau ký = phụ phí.

---

## References

- `references/shooting_proposal_template.pptx` — Template PowerPoint Shooting Proposal
- `references/bao_gia_template.md` — Báo giá dạng markdown
- `references/bao_gia_template.csv` — Báo giá dạng spreadsheet
- `references/pdf-image-extraction-pipeline.md` — Pipeline trích xuất nội dung từ PDF image-based (designer PDFs)

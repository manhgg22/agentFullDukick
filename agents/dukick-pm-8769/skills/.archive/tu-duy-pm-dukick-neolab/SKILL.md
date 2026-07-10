---
name: tu-duy-pm-dukick-neolab
title: Tư duy PM DUKICK & NeoLab - Theo dõi đối thủ TVC AI Việt Nam
trigger: |
  Khi cần thiết lập hoặc thực hiện theo dõi đối thủ sản xuất TVC/Video AI tại Việt Nam,
  hoặc khi user yêu cầu "tạo cronjob theo dõi đối thủ TVC AI".
description: |
  Quy trình chuẩn để PM DUKICK tự động theo dõi đối thủ thị trường TVC AI (AI thuần và AI Hybrid)
  tại Việt Nam. Bản tin tình báo thị trường ngắn, đều, có bảng theo dõi đối thủ.
  Mục tiêu: mở ra 5-10 phút là biết ai đang làm gì, họ bán như thế nào, có gì đáng lo, Dukick nên phản ứng ra sao.
  Chu kỳ: 2 bản/tuần — Thứ Hai và Thứ Năm lúc 10:00.
---

# Tư duy PM DUKICK & NeoLab: Theo dõi đối thủ TVC AI Việt Nam

## Mục tiêu
Mỗi tuần 2 bản (Thứ Hai và Thứ Năm lúc 10:00), tự động thu thập và tổng hợp thông tin thị trường TVC AI để PM nắm bắt:
- Đối thủ cạnh tranh trực tiếp/gián tiếp
- Xu hướng công nghệ AI trong sản xuất video
- Case study/campaign nổi bật
- Cơ hội, rủi ro và đề xuất hành động cho DUKICK/NeoLab

**Nguyên tắc:** Bản tin tình báo thị trường ngắn, đều, có bảng theo dõi đối thủ. Không viết dài như report nghiên cứu. Mục tiêu là để bạn mở ra trong 5-10 phút là biết: ai đang làm gì, họ bán như thế nào, có gì đáng lo, Dukick nên phản ứng ra sao.

## Logic lịch quét
- **Bản thứ Hai 10:00**: quét từ **10:00 thứ Năm tuần trước → 10:00 thứ Hai hiện tại**.
- **Bản thứ Năm 10:00**: quét từ **10:00 thứ Hai hiện tại → 10:00 thứ Năm hiện tại**.

## Bố cục báo cáo chuẩn (bản tin tình báo)

### 1. TÓM TẮT NHANH
5-7 gạch đầu dòng quan trọng nhất:
- Đối thủ nào mới xuất hiện
- Ai vừa ra sản phẩm/case mới
- Thị trường đang nói gì về TVC AI/AI Hybrid

### 2. BẢNG ĐỐI THỦ / CÔNG TY ĐÁNG CHÚ Ý
| Tên đơn vị | Loại hình | Dịch vụ AI/TVC | Case study/Nội dung mới | Khách hàng/Brand | Điểm mạnh đang claim | Mức độ đe dọa với Dukick | Link nguồn |
|---|---|---|---|---|---|---|---|

Loại hình gợi ý: production house, agency, freelancer team, AI studio, post/VFX, animation, marketing agency

### 3. TÍN HIỆU THỊ TRƯỜNG
- TVC AI giá rẻ đang được quảng cáo nhiều hơn?
- AI Hybrid đang được dùng cho storyboard, animatic, mockup hay final output?
- Khách hàng SME, startup, brand lớn hay agency đang quan tâm?
- Có bên nào dùng "AI TVC trong 24h/48h/giá rẻ" làm thông điệp bán hàng không?

### 4. CASE / CHIẾN DỊCH NỔI BẬT TRONG TUẦN
Chọn 1-3 case nếu có:
- Nội dung/campaign là gì
- Mức độ AI có vẻ được dùng ở đâu: concept, visual, motion, voice, edit, VFX, full AI
- Chất lượng cảm nhận
- Bài học cho Dukick

### 5. THÔNG ĐIỆP BÁN HÀNG CỦA ĐỐI THỦ
Theo dõi cách họ chào bán:
- "Nhanh hơn"
- "Rẻ hơn"
- "Không cần quay"
- "AI + production team"
- "TVC viral/social-first"
- "AI storyboard/AI previsualization"

Mục này quan trọng để Dukick biết thị trường đang bị educate theo hướng nào.

### 6. CƠ HỘI CHO DUKICK
3-5 gợi ý hành động:
- Nên làm content gì
- Nên đóng gói dịch vụ AI Hybrid ra sao
- Nên follow khách hàng/sector nào
- Có nên phản ứng với claim của đối thủ không

### 7. RỦI RO CẦN THEO DÕI
- Đối thủ phá giá
- Chất lượng AI thấp nhưng bán rất mạnh
- Agency tự build in-house AI production
- Client hiểu nhầm "AI TVC = không cần production"
- Vấn đề bản quyền/giọng nói/hình ảnh người thật

### 8. DANH SÁCH NGUỒN ĐÃ QUÉT
Nên gồm link trực tiếp từ:
- Website công ty
- Facebook/LinkedIn/TikTok/YouTube/Vimeo/Behance
- Báo chí/ngành quảng cáo
- Google search kết quả mới
- Marketplace/freelancer nếu thấy liên quan

## Quy trình thực hiện

### Bước 0: Đọc template mẫu từ Leo🌷 (nếu có)
- Leo🌷 thường gửi file `message.txt` hoặc văn bản định nghĩa **bố cục chuẩn** cho báo cáo
- **Luôn đọc file này trước** khi tạo hoặc cập nhật cronjob — không tự ý sáng tạo bố cục
- Mẫu tham khảo đã được lưu tại: `references/bao-cao-tvc-ai-template.md`

### Bước 1: Duyệt bố cục với Leo🌷
- Trình bày đề xuất bố cục (như trên)
- Chờ chị Leo duyệt trước khi triển khai
- **Không tự ý chạy nếu chưa được duyệt**

### Bước 2: Tạo cronjob cho từng PM
- Mỗi PM (Thái, Huyền, Hoàng) có cronjob riêng
- Lịch chạy: Thứ Hai và Thứ Năm lúc 10:00 sáng
- Gửi kết quả vào thread riêng của từng người trên Discord
- Thread ID tham khảo:
  - Thái: `1407966179758182447`
  - Huyền: `1511955929615040573`
  - Hoàng: `1349587719424180294`

### Bước 3: Thu thập dữ liệu
**Tỷ lệ phân bổ nỗ lực tìm kiếm:**
- **Facebook — 40%** (quan trọng nhất, kênh rất sôi động):
  - Tìm các trang Facebook public của đối thủ: site:facebook.com + [tên công ty] + "TVC AI"
  - Tìm các group Facebook công khai: "TVC AI Việt Nam", "AI Video", "Sản xuất video AI"
  - Tìm các bài post public về TVC AI: site:facebook.com + "TVC AI" + "video" + date filter
  - Theo dõi page của: ME Group, MAY Production, ECHO, ColorMedia, GiaPhái, các freelancer AI video
  - Tìm các post bán hàng/dịch vụ TVC AI trên Facebook Marketplace/groups

- **Website công ty — 20%**: Portfolio, landing page, blog, case study
- **Báo chí/ngành — 20%**: Dân trí, Báo Đầu Tư, Pháp Luật TP.HCM, CafeF, Vietnamnet...
- **YouTube/Vimeo/Behance — 10%**: Demo reel, case study video, portfolio motion
- **LinkedIn/TikTok — 10%**: Company updates, viral content, behind-the-scenes

Công cụ sử dụng:
- **Web search**: Google, Bing với từ khóa tiếng Việt + tiếng Anh
- **Exa Search**: Neural search chuyên sâu về công ty, case study
- **Firecrawl**: Crawl website đối thủ, portfolio, landing page
- **Documentation Lookup**: Tra cứu công nghệ AI mới (Sora, Runway, Kling, Veo 3...)
- **Social scan**: YouTube, Facebook, Instagram, LinkedIn, TikTok, Vimeo, Behance (nếu có dữ liệu)

### Bước 4: Tổng hợp và gửi báo cáo
- Viết báo cáo theo đúng 8 mục bố cục đã duyệt
- Dùng tiếng Việt thuần, chỉ dùng từ tiếng Anh khi thực sự cần thiết
- Phân biệt rõ: **đã xác nhận từ nguồn** vs **nhận định/suy luận**
- Chấm mức ảnh hưởng với Dukick cho từng đối thủ
- Nếu không có tin mới, vẫn cập nhật "không thấy biến động lớn" và nêu các nguồn đã kiểm tra
- Gửi vào đúng thread Discord của PM
- Lưu bản sao vào file local nếu cần

### Bước 5: Theo dõi và cải tiến
- Hàng tuần review chất lượng báo cáo với Leo🌷
- Điều chỉnh prompt/từ khóa nếu kết quả chưa đạt
- Cập nhật skill này khi quy trình thay đổi

## Các từ khóa tìm kiếm đề xuất
- "TVC AI Việt Nam", "AI video production Vietnam"
- "Sora commercial Vietnam", "Runway TVC campaign"
- "AI hybrid video ad", "generative AI advertising Vietnam"
- "production house AI", "AI filmmaking Vietnam 2025"
- "Veo 3 TVC", "Kling video", "Seedance AI"
- "sản xuất video AI", "TVC giá rẻ AI", "AI Hybrid Production"
- "AI TVC 24h", "AI TVC 48h", "AI TVC nhanh rẻ"
- "AI storyboard", "AI previsualization", "AI animatic"

## Lưu ý quan trọng

### Xử lý file template từ Leo🌷
- Leo🌷 thường gửi file `message.txt` hoặc văn bản đính kèm để định nghĩa **bố cục chuẩn** cho báo cáo
- **Luôn đọc file đính kèm trước** — không tự ý sáng tạo bố cục khác
- Nếu Leo🌷 nói "stop" → dừng ngay việc giải thích/thuyết trình, chuyển sang **thực hiện đúng format** họ đưa ra
- Template tham khảo đã lưu tại: `references/bao-cao-tvc-ai-template.md`

### Style báo cáo
- **Ngắn, đều, có bảng** — không viết dài như report nghiên cứu
- **Mục tiêu**: mở ra trong 5-10 phút là biết ai đang làm gì, họ bán như thế nào, có gì đáng lo, Dukick nên phản ứng ra sao
- **Phân biệt rõ**: đã xác nhận từ nguồn vs nhận định/suy luận
- **Nếu không có tin mới**: vẫn cập nhật "không thấy biến động lớn" + nêu nguồn đã kiểm tra
- **Chấm mức ảnh hưởng** với Dukick cho từng đối thủ
- **Tiếng Việt thuần**, chỉ dùng từ tiếng Anh khi thực sự cần

### Quy trình triển khai
- **Chỉ gửi báo cáo vào thread riêng**, không spam kênh chính
- **Chờ duyệt bố cục trước** khi tạo cronjob (nhưng nếu Leo🌷 đã gửi file mẫu → coi như đã duyệt, triển khai ngay)
- **Dùng nhiều nguồn** (web, Exa, Firecrawl, social) để đảm bảo đầy đủ
- **Cập nhật skill** khi quy trình thay đổi theo yêu cầu của Leo🌷
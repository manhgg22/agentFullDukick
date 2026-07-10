---
name: strategic-analysis
description: >
  Đánh giá chiến lược, phân tích khả thi, và đề xuất phương án cho CEO.
  Dùng khi chị Leo hoặc anh Nam yêu cầu "tư duy tổng thể", đánh giá option,
  hoặc quyết định giữa nhiều hướng đi.
triggers:
  - Tư duy tổng thể
  - Đánh giá khả thi
  - Cần làm gì, làm thế nào
  - So sánh phương án / lựa chọn
  - Mức độ khả thi
---

# Strategic Analysis — Đánh Giá Chiến Lược & Khả Thi

## Khi nào dùng
Khi CEO (chị Leo hoặc anh Nam) yêu cầu phân tích tổng thể một vấn đề, đánh giá nhiều phương án, hoặc đưa ra khuyến nghị chiến lược. Đặc biệt phổ biến với các từ khóa: "tư duy tổng thể", "cần làm gì, làm thế nào", "mức độ khả thi".

## Cấu trúc phản hồi chuẩn (6 phần)

### 1. TÓM TẮT YÊU CẦU
- Người yêu cầu, mục đích, ngữ cảnh hiện tại
- Phạm vi (scope) rõ ràng — giới hạn "trước mắt" vs "tương lai"

### 2. PHÂN TÍCH HIỆN TRẠNG
- Đọc vault **tất cả bộ phận liên quan** trước khi trả lời
- Tìm: incident lịch sử, plan cũ, SOP hiện có, trạng thái công nghệ, log Discord
- **Không giả định** — chỉ dùng dữ liệu vault + kiến thức xác nhận được
- Nếu thiếu data → ghi rõ "chưa có data" thay vì ước tính

### 3. CÁC PHƯƠN ÁN (≥2)
Mỗi phương án phải có:
| Phương án | Cách làm | Ưu điểm | Nhược điểm | Khả thi |
|-----------|----------|---------|------------|---------|
| A — ... | ... | ... | ... | 🟢/🟡/🔴 |

- **A**: Phương án chính thống / API / chuẩn (thường khuyến nghị)
- **B**: Phương án workaround / automation / rủi ro cao (thường không khuyến nghị)
- **C**: Phương án hybrid / duyệt thủ công trước khi auto (thường an toàn nhất)

### 4. ĐỀ XUẤT & LÝ DO
- Chọn 1 phương án khuyến nghị (thường là C — hybrid)
- Giải thích ngắn gọn tại sao chọn phương án đó
- Liên hệ với tình trạng thực tế của Dukick: incident lịch sử, SOP, data readiness

### 5. LỘ TRÌNH TRIỂN KHAI
| Bước | Công việc | Người phụ trách | Deadline đề xuất |
|------|-----------|-----------------|-----------------|

### 6. RỦI RO & QUYẾT ĐỊNH CẦN CEO
- Rủi ro nổi bật (≤5 điểm)
- Các câu hỏi cụ thể cần CEO quyết định ngay

## Nguyên tắc
- **Vault-first**: Luôn đọc vault trước, không dựa vào giả định
- **No-assumption**: Khi thiếu data, ghi rõ "chưa có data"
- **CEO-ready**: Format dễ scan — bảng, emoji, bullet points. Không dài dòng.
- **Tied to Dukick context**: Mỗi đề xuất liên hệ với incident, SOP, Hermes status
- **Options with pros/cons**: Luôn đưa ra ≥2 lựa chọn rõ ràng

## Nhắc việc follow-up
Nếu CEO yêu cầu "nhắc lại đến khi xong" → dùng skill `leo-daily-sync` (Kiểu B — Periodic Reminder) để tạo cronjob follow-up. Xem `references/periodic-reminder-setup.md` trong skill `leo-daily-sync`.

## Pitfalls
- Đừng đưa ra chỉ 1 phương án — CEO luôn cần ≥2 lựa chọn để so sánh
- Đừng bỏ qua bước "rủi ro" — CEO cần biết trước khi quyết
- Đừng gom quá nhiều phương án (tối đa 3–4, mỗi cái phải khác biệt rõ rệt)
- Đừng để deadline/owner trống trong lộ trình
- Đừng quên đọc vault **NeoLab** (tài chính) và **HR** khi phân tích có liên quan
- Đừng quên kiểm tra **incident lịch sử** trên cùng nền tảng trước khi đề xuất automation

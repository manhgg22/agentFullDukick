---
name: hr-personnel-evaluation
category: hr
description: >
  Đánh giá nhân sự mới trong giai đoạn thử việc hoặc chuyển vị trí.
  Bao gồm: phân tích xung khắc tính cách-vị trí, xây dựng kế hoạch test có tiêu chí,
  giám sát chéo bằng AI + người, đánh giá đa kịch bản, đề xuất phương án backup.
triggers:
  - BOD hoặc HR yêu cầu đánh giá nhân sự mới / thử việc
  - Nhận thấy xung khắc giữa tính cách ứng viên và yêu cầu công việc
  - Cần thiết lập tiêu chí đánh giá thử việc có giới hạn rủi ro
  - Đề xuất khai thác điểm mạnh khác của nhân sự song song với vị trí chính
---

# HR Personnel Evaluation — Đánh Giá & Test Nhân Sự

## Nguyên tắc cốt lõi

1. **Chỉ phản hồi khi được trigger.** Không tự động chào hỏi, không nói lan man.
2. **AI là công cụ giám sát, không thay thế người.** Mọi quyết định tuyển dụng / sa thải / điều chuyển thuộc về BOD.
3. **Minh bạch khi BOD yêu cầu.** Công khai mô hình test với nhân sự nếu BOD chỉ định.
4. **Không bịa đặt tiêu chí.** Luôn đối chiếu với JD có sẵn trong vault trước khi đánh giá.

## Workflow 4 bước

### Bước 1: Phân tích xung khắc tính cách ↔ Vị trí

- Đọc JD (mô tả công việc) từ vault — dùng `search_files` hoặc `read_file`.
- Liệt kê yêu cầu phẩm chất cốt lõi của vị trí (vd: tỉ mỉ, chính xác, kiên trì lặp lại).
- Đối chiếu với đặc điểm tính cách nhân sự do BOD/HR mô tả.
- Nếu phát hiện xung khắc → ghi nhận rõ ràng, không che giấu.

**Template ghi nhận:**

| Vị trí cần | Phẩm chất yêu cầu | Nhân sự có | Đánh giá |
|-----------|-------------------|------------|----------|
| Kế toán | Tỉ mỉ, chính xác | Tham vọng, nhìn rộng | ⚠️ Xung khắc tiềm ẩn |

### Bước 2: Xây dựng kế hoạch test có giới hạn rủi ro

**Cấu trúc tuần làm việc (mẫu):**

| Ngày | Nội dung chính | Giám sát |
|------|---------------|----------|
| Thứ 2 | Task chính (vd: dòng tiền, chứng từ) | AI kiểm tra chéo |
| Thứ 3 | Task chính tiếp theo | AI rà soát |
| Thứ 4 | **Ngày khai thác điểm mạnh thứ 2** (vd: BD, research) | BOD nhận báo cáo list |
| Thứ 5 | Task chính | AI kiểm tra chéo |
| Thứ 6 | Tổng kết tuần | AI tổng hợp đánh giá |

**Giới hạn rủi ro tài chính:**
- Tuần 1-4: Không chuyển tiền thực / chỉ test.
- Tuần 5-6: Chuyển tiền nhỏ (<10 triệu) với approval BOD.
- AI kiểm tra 100% chứng từ trước chuyển tiền.
- Người hiện tại giữ quyền veto / standby.

### Bước 3: Giám sát chéo AI + Người

**AI HuongHR đảm nhiệm:**
- Đối chiếu số liệu sổ quỹ vs sao kê ngân hàng.
- Kiểm tra tính đầy đủ chứng từ trước thanh toán.
- Nhắc deadline trước 3-7 ngày.
- Tổng hợp báo cáo đánh giá tuần.

**Người hiện tại đảm nhiệm:**
- Double-check trước khi nộp thuế / BCTC.
- Standby xử lý nếu nhân sự nghỉ đột ngột.
- Audit ngẫu nhiên hàng tháng.

**Điều kiện AI hoạt động:**
Nhân sự hoặc BOD phải **gửi dữ liệu đầu vào** cho AI (báo cáo Excel/PDF). AI không tự truy cập hệ thống kế toán.

### Bước 4: Đánh giá đa kịch bản (sau n tuần)

**Bảng đánh giá tổng hợp (template):**

| Tiêu chí | Trọng số | Tuần 2 | Tuần 4 | Tuần 6 | Tuần 8 |
|----------|----------|--------|--------|--------|--------|
| Task chính — chính xác | 30% | /10 | /10 | /10 | /10 |
| Task chính — tỉ mỉ | 20% | /10 | /10 | /10 | /10 |
| Task chính — dự báo rủi ro | 15% | /10 | /10 | /10 | /10 |
| Task chính — deadline | 10% | /10 | /10 | /10 | /10 |
| Task phụ — số lượng output | 10% | /10 | /10 | /10 | /10 |
| Task phụ — chất lượng | 10% | /10 | /10 | /10 | /10 |
| Communication | 5% | /10 | /10 | /10 | /10 |
| **TỔNG** | **100%** | | | | |

**Ngưỡng xét:**
- ≥ 70%: Đạt chính thức / chuyển vị trí phù hợp.
- 50-69%: Xem xét kéo dài thử việc thêm 1 tháng.
- < 50%: Không đạt — kích hoạt phương án backup.

**4 kịch bản kết quả:**

| Kịch bản | Task chính | Task phụ | Phương án |
|----------|-----------|----------|-----------|
| A | Đạt | Đạt | Task chính chính thức + task phụ hỗ trợ (20-30% thời gian) |
| B | Đạt | Không đạt | Tập trung 100% task chính |
| C | Không đạt | Đạt | **Chuyển ngay sang task phụ** — đã có data thử việc |
| D | Không đạt cả hai | | Kết thúc thử việc, người hiện tại take over |

## Pitfalls

1. **Để nhân sự làm task chính 100% thời gian khi đã phát hiện xung khắc** → Lãng phí thời gian cả hai bên, mất cơ hội khai thác điểm mạnh.
2. **Không thiết lập quyền truy cập giới hạn trong tuần đầu** → Rủi ro mất kiểm soát tài chính.
3. **AI giám sát mà không có dữ liệu đầu vào** → AI trở thành vô dụng. Phải yêu cầu BOD hoặc nhân sự gửi báo cáo.
4. **Không chuẩn bị phương án backup trước khi bắt đầu** → Nếu nhân sự nghỉ đột ngột giữa chừng, công việc tài chính bị đứt gãy.
5. **Nói lan man, tự động chào hỏi khi chưa được trigger** → Vi phạm quy tắc trigger-only của BOD.

## References

- `references/personnel-evaluation-checklist.md` — Checklist hành động HR từng tuần
- `templates/weekly-evaluation-form.md` — Template báo cáo đánh giá hàng tuần
- `templates/4-scenario-decision-matrix.md` — Ma trận quyết định 4 kịch bản

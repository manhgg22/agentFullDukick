---
name: production-finance-ops
description: Finance operations for Dukick Film — cronjob reminders, PPW tracking, Discord tagging, job cashflow, tax deadlines.
triggers:
  - "Dukick finance daily reminder"
  - "cronjob nhắc việc kế toán"
  - "bảng PPW thu chi"
  - "nhắc việc sản xuất thanh toán"
  - "tag discord kế toán PM GĐTC"
---

# Production Finance Ops — Dukick

Skill này quản lý toàn bộ workflow tài chính + reminder hàng ngày cho công ty sản xuất phim Dukick.

## Data Source

**QUAN TRỌNG — Nguồn dữ liệu duy nhất được coi là đúng:**
Bảng **QUẢN TRỊ PPW - THU - CHI** được duy trì trực tiếp trên **Google Sheets online** (không phải file `.md` local). File `.md` trong Obsidian Vault là bản snapshot cũ — KHÔNG dùng làm source-of-truth.

→ Luôn yêu cầu người dùng cung cấp **link Google Sheets** hoặc **CSV export URL** (`/export?format=csv`) trước khi đọc dữ liệu.

## Discord User IDs (để tag đúng người)

| Vai trò | Tên | Discord ID | Trạng thái |
|---------|-----|------------|-----------|
| Kế toán | Yến | `885170747797032991` | ✅ |
| Kế toán | Hương | `880750919304749096` | ✅ |
| PM | Huyền | `1338069800240549898` | ✅ |
| PM/SX | Thái | `1406146356006879313` | ✅ |
| PM/SX | Hoàng | `765590233601015849` | ✅ |
| GĐTC | Chị Leo (Nhật Phương) | `1091125381421072425` | ✅ |
| GĐSX | Anh Gia Nam | TBD | ⏳ Chờ |

Khi chưa có ID, ghi rõ tên thay vì tag chung chung.

## Cronjob Daily Reminder — Cấu hình

Tạo cronjob chạy **mỗi ngày 9:00 sáng** (`0 9 * * *`), deliver về kênh origin.

### Nội dung message gửi mỗi sáng:

1. **Tổng quan** — số job có hoạt động tuần này, số thanh toán đến hạn, cảnh báo đỏ.
2. **🔴 SX / PM** — Shooting day, BBNT deadlines, final delivery, production milestones. Tag `<@1338069800240549898>` (Huyền) + Thái/Hoàng khi có ID.
3. **🟡 EP / GĐTC** — Budget approvals, contract signings, payment approvals, NDA. Tag chị Nhật Phương khi có ID.
4. **🔵 Kế toán / Tài chính** — Invoice issuance, payment execution, ĐNTT, tax deadlines, settlement/quyết toán. Tag `<@885170747797032991>` (Yến).

### Urgency flags trong reminder:

| Emoji | Ý nghĩa | Thời hạn |
|-------|---------|----------|
| 🔥 | Gấp | Hôm nay hoặc quá hạn |
| ⚡ | Sắp | Trong 3 ngày tới |
| 📅 | Lên lịch | 4–7 ngày tới |

### Footer bắt buộc:

> *Finance Bot chỉ hỗ trợ nhắc việc — mọi quyết định duyệt chi/thanh toán vui lòng liên hệ trực tiếp GĐTC và Kế toán.*

## Workflow PPW (Brief → Ký HĐ → Duyệt dự trù → Tạm ứng → Sản xuất → BBNT → ĐNTT → HĐ → Thanh toán)

| Cột theo dõi | Ý nghĩa | Người liên quan |
|--------------|---------|-----------------|
| HĐ | Hợp đồng | EP/GĐTC duyệt |
| ĐNTT | Đề nghị thanh toán | PM/SX gửi, Kế toán xử lý |
| BBNT | Biên bản nghiệm thu | PM/SX làm, khách ký |
| HĐ nháp | Hóa đơn nháp | Kế toán lập |
| HĐ chính thức | Hóa đơn GTGT phát hành | Kế toán |
| Thanh toán | Chuyển khoản | Kế toán thực hiện, EP/GĐTC duyệt trước |

**Màu sắc trong bảng:**
- **Đỏ** = ngày thanh toán
- **Xanh** = ngày shooting / hoàn thiện job

## Nguyên tắc Khi Đọc Bảng PPW

1. Phân biệt rõ **Thu** (doanh thu từ khách) và **Chi** (chi phí sản xuất + thanh toán freelancer).
2. Đối chiếu cột theo tuần: deadline nào rơi vào tuần hiện tại hoặc tuần tới.
3. Với mỗi job, kiểm tra:
   - Đã thu / còn phải thu
   - Đã chi / còn phải chi
   - Freelancer cần thanh toán
   - Chứng từ đủ chưa
   - Đã quyết toán chưa

## Quy tắc Tạm Ứng Chi Phí Sản Xuất

- **Mức tối đa:** 20% dự trù ngân sách
- **Được tạm ứng:** Art, Catering, Bối cảnh
- **KHÔNG được tạm ứng:** Nhân sự, Thuê thiết bị
- **Ngoại lệ 7 ngày:** Runner, Diễn viên, Art support (xem xét riêng)
- **Phát sinh lớn hoặc thanh toán bất thường:** Báo trước ít nhất 7 ngày

## Quy trình nghiệm thu job (Bắt buộc)

Khi bàn giao job, PM phải cung cấp đủ deliverable theo checklist từng loại:

### Nghiệm thu tổng quan (mọi job)
| # | Nội dung | Ghi chú |
|---|----------|---------|
| 1 | File final đúng format + brief | Theo timeline đã duyệt |
| 2 | Shot list / storyboard hoàn chỉnh | Ghi rõ phát sinh nếu có |
| 3 | BBNT có chữ ký KH | Bản mềm → KH confirm → bản cứng |
| 4 | Hóa đơn VAT chính thức | Theo tiến độ HĐ |
| 5 | Lưu trữ tài liệu đầy đủ trên Drive | Có quyền truy cập cho KT |

### Riêng mảng AI dùng cho sản xuất job
Khi job sử dụng công cụ AI hoặc mua credit AI, PM **bắt buộc** cung cấp:

| Giai đoạn | Minh chứng |
|-----------|------------|
| **Mua / nạp credit** | Ảnh chụp màn hình tài khoản AI lúc vừa mua/nạp (hiển thị rõ số dư credit ban đầu, ngày giao dịch, tên tài khoản) |
| **Sau khi hoàn thành job** | Ảnh chụp màn hình tài khoản AI còn lại (số credit còn, đối chiếu lượng tiêu thụ) |

> Lưu ảnh vào folder dự án trên Drive ngay khi chụp, đặt tên rõ ràng.

**Chế tài nếu thiếu minh chứng AI:**
- Công ty **không thanh toán** các khoản chi phí AI của job.
- Yêu cầu **hoàn lại toàn bộ con số tạm ứng** đã chi trước đó (nếu có).
- Trường hợp đặc biệt: có văn bản giải trình + phê duyệt từ Giám đốc.

## Pitfalls

1. **Đừng dùng file `.md` local làm nguồn đúng** — luôn hỏi link Google Sheets.
2. **Đừng tag role chung chung** — tag đúng Discord ID từng người.
3. **Đừng tự suy luận deadline** — chỉ đọc từ bảng, không đoán.
4. **Chưa đủ chứng từ = chưa ghi nhận chi** — không tự ý thêm khoản chi khi thiếu HĐ/BBNT/Hóa đơn.
5. **Job xong 5 ngày = phải quyết toán** — nhắc PM/SX ngay sau onset.
6. **Không ghi số tiền cố định trong chế tài** — mỗi job có con số tạm ứng khác nhau, ghi "hoàn lại toàn bộ con số tạm ứng" thay vì ghi số cụ thể (ví dụ "4 triệu").
7. **Tránh nội dung thừa thãi** — khi user yêu cầu ghi quy trình, chỉ ghi đúng nội dung bắt buộc. Không tự thêm phần "đề xuất bổ sung", "khuyến nghị", hay bảng mở rộng nếu user không yêu cầu. Tập trung vào yêu cầu cốt lõi.

## References

- `references/ppw-column-guide.md` — Giải thích chi tiết từng cột trong bảng PPW
- `references/discord-id-mapping.md` — Bảng mapping Discord ID nhân sự (update liên tục)
- `references/ai-job-acceptance-checklist.md` — Minh chứng AI cho nghiệm thu job (session-specific, 26/06/2026)
- `templates/daily-reminder-message.md` — Template message nhắc việc hàng ngày

## When to Update This Skill

- Khi có thêm Discord ID nhân sự mới → cập nhật `references/discord-id-mapping.md`
- Khi bảng PPW thêm cột mới hoặc đổi format → cập nhật `references/ppw-column-guide.md`
- Khi quy trình tạm ứng / thanh toán thay đổi → patch SKILL.md
- Khi có thêm quy định nghiệm thu job mới → patch SKILL.md
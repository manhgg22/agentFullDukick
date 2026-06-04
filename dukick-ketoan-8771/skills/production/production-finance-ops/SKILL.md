---
name: production-finance-ops
description: Finance operations for DuKick Film — cronjob reminders, PPW tracking, Discord tagging, job cashflow, tax deadlines.
triggers:
  - "dukick finance daily reminder"
  - "cronjob nhắc việc kế toán"
  - "bảng PPW thu chi"
  - "nhắc việc sản xuất thanh toán"
  - "tag discord kế toán PM GĐTC"
---

# Production Finance Ops — DuKick

Skill này quản lý toàn bộ workflow tài chính + reminder hàng ngày cho công ty sản xuất phim DuKick.

## Data Source

**QUAN TRỌNG — Nguồn dữ liệu duy nhất được coi là đúng:**
Bảng **QUẢN TRỊ PPW - THU - CHI** được duy trì trực tiếp trên **Google Sheets online** (không phải file `.md` local). File `.md` trong Obsidian Vault là bản snapshot cũ — KHÔNG dùng làm source-of-truth.

→ Luôn yêu cầu người dùng cung cấp **link Google Sheets** hoặc **CSV export URL** (`/export?format=csv`) trước khi đọc dữ liệu.

## Discord User IDs (để tag đúng người)

| Vai trò | Tên | Discord ID | Trạng thái |
|---------|-----|------------|-----------|
| Kế toán | Yến | `885170747797032991` | ✅ Đã có |
| PM | Huyền | `1338069800240549898` | ✅ Đã có |
| PM/SX | Thái | TBD | ⏳ Chờ |
| PM/SX | Hoàng | TBD | ⏳ Chờ |
| GĐTC | Chị Nhật Phương | TBD | ⏳ Chờ |

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

## Pitfalls

1. **Đừng dùng file `.md` local làm nguồn đúng** — luôn hỏi link Google Sheets.
2. **Đừng tag role chung chung** — tag đúng Discord ID từng người.
3. **Đừng tự suy luận deadline** — chỉ đọc từ bảng, không đoán.
4. **Chưa đủ chứng từ = chưa ghi nhận chi** — không tự ý thêm khoản chi khi thiếu HĐ/BBNT/Hóa đơn.
5. **Job xong 5 ngày = phải quyết toán** — nhắc PM/SX ngay sau onset.

## References

- `references/ppw-column-guide.md` — Giải thích chi tiết từng cột trong bảng PPW
- `references/discord-id-mapping.md` — Bảng mapping Discord ID nhân sự (update liên tục)
- `templates/daily-reminder-message.md` — Template message nhắc việc hàng ngày

## When to Update This Skill

- Khi có thêm Discord ID nhân sự mới → cập nhật `references/discord-id-mapping.md`
- Khi bảng PPW thêm cột mới hoặc đổi format → cập nhật `references/ppw-column-guide.md`
- Khi quy trình tạm ứng / thanh toán thay đổi → patch SKILL.md

# PPW Column Guide — Bảng QUẢN TRỊ PPW - THU - CHI

## Cấu trúc tổng quan

Bảng PPW (Production Planning & Wallet) theo dõi luồng thu-chi của từng job theo **tuần** (weekly columns).

## Các cột công việc theo tuần

| Ký hiệu | Ý nghĩa đầy đủ | Người phụ trách | Mô tả |
|---------|---------------|-----------------|-------|
| **HĐ** | Hợp đồng | EP / GĐTC | Ký hợp đồng với khách hàng. Bắt buộc trước khi sản xuất. |
| **ĐNTT** | Đề nghị thanh toán | PM/SX gửi, Kế toán xử lý | PM gửi email đề nghị thanh toán, đính kèm HĐ + BBNT + hóa đơn. |
| **BBNT** | Biên bản nghiệm thu | PM/SX | Xác nhận khách hàng đã nhận và duyệt sản phẩm. Ký 2 bên. |
| **HĐ nháp** | Hóa đơn nháp | Kế toán | Nháp hóa đơn GTGT để khách kiểm tra thông tin. |
| **HĐ chính thức** | Hóa đơn GTGT chính thức | Kế toán | Phát hành hóa đơn điện tử chính thức. |
| **Thanh toán** | Chuyển khoản | Kế toán | Thực hiện thanh toán theo HĐ. |

## Luồng công việc một job điển hình

```
Brief → Ký HĐ → Duyệt dự trù → Tạm ứng → Sản xuất → BBNT → ĐNTT → HĐ nháp → HĐ chính thức → Thanh toán
```

## Màu sắc trong bảng (Quan trọng)

| Màu | Ý nghĩa |
|-----|---------|
| 🔴 **Đỏ** | Ngày **thanh toán** |
| 🟢 **Xanh** | Ngày **shooting** hoặc **hoàn thiện job (final)** |
| Bold + IN HOA | Ngày quan trọng, bắt buộc |

## Cách đọc deadline từ bảng

1. Tìm job cần theo dõi ở cột đầu tiên
2. Quét ngang theo tuần → tìm ô có màu hoặc ngày cụ thể
3. So sánh ngày đó với hôm nay:
   - = hôm nay hoặc quá hạn → 🔥 Gấp
   - ≤ 3 ngày tới → ⚡ Sắp
   - 4–7 ngày tới → 📅 Lên lịch

## Các job hiện có (theo dữ liệu 2026-06-04)

| STT | Tên job | Loại | Ghi chú |
|-----|---------|------|---------|
| 1 | Nomad Teaser Đồ Sơn | Teaser | 2 đợt thanh toán |
| 2 | Nomad 3D Đồ Sơn | 3D | 2 đợt thanh toán |
| 3 | The One | Video | Nhiều clip, nhiều đợt |
| 4 | Sun - Alaso | ? | Thanh toán full |
| 5 | HNS 5 clips | 5 clips | 3 đợt thanh toán |
| 6 | VNG | ? | Thanh toán full |
| 7 | May10 | Clip | 2 đợt |

## Dòng "CÒN LẠI" (dòng tổng)

Dòng cuối bảng hiển thị **số dư tạm tính** còn lại theo từng tuần. Nếu số giảm mạnh = dòng tiền đang ra nhiều → cảnh báo EP/GĐTC.

## When to update this guide
- Bảng PPW thêm cột mới hoặc đổi cấu trúc
- Thêm job mới vào tracking
- Thay đổi quy trình thu/chi (ví dụ: thêm bước kiểm soát nội bộ)

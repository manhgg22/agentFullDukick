# Chi tiêu & Nhắc Nộp Bill — Reference

## Mục đích

Hướng dẫn Agent Tổng theo dõi các khoản chi phí cần duyệt, đã duyệt, đã chuyển khoản — và tự động nhắc nộp bill cho HR (chị Hương Nguyễn) vào ngày hôm sau.

## File theo dõi

- **Vị trí:** `C:\Users\Admin\Documents\Obsidian Vault\Dukick-Tong\Theo-Doi-Chi-Tieu.md`
- **Cập nhật:** Mỗi lần phát hiện tin nhắn xin duyệt chi trên Discord.
- **Đọc/ghi:** Dùng `execute_code` + Python (Windows path workaround).

## Cấu trúc file

3 bảng theo dõi:

1. **🔄 Đang chờ duyệt** — Khi nhận tin nhắn xin duyệt
2. **✅ Đã duyệt / Chờ chuyển khoản** — Khi chị Leo duyệt
3. **💰 Đã chuyển khoản / Chờ bill** — Khi xác nhận CK thành công → nhắc bill ngày hôm sau

## Pattern nhận diện trạng thái từ Discord

| Tín hiệu trong chat | Hành động |
|---------------------|-----------|
| "xin duyệt chi" / "duyệt chi phí" | Thêm vào bảng "Đang chờ duyệt" |
| "ok" / "chốt" / "ck rồi nhé" từ chị Leo | Di chuyển sang "Đã duyệt" |
| "đã chuyển" / "ck thành công" / "đã thanh toán" | Di chuyển sang "Đã CK", lên lịch nhắc bill |
| "gửi bill" / "nhận bill rồi" từ HR | Cập nhật "Bill đã nhận" + ngày |

## Script nhắc bill đơn giản

```python
from hermes_tools import send_message

# Đọc file tracking
# Tìm các khoản "Đã CK / Chờ bill" chưa được nhắc
# Gửi nhắc nhở vào kênh gốc (hoặc DM)
# Cập nhật cột "Đã nhắc" = ngày nhắc

# Ví dụ message:
"""
@Duck Mẹn Khoản chi Ollama Max+ + ChatGPT Plus — 3.400.000 VND
đã được chuyển khoản. Vui lòng gửi bill thanh toán cho chị Hương Nguyễn (HR)
để lưu chứng từ nhé.
"""
```

## Lưu ý

- Người xin duyệt chi **vẫn phải** tuân thủ quy tắc tag chị Leo (`CẦN CHỊ LEO DUYỆT` + like).
- Nếu không có bill → HR không lưu được chứng từ → agent tiếp tục nhắc cho đến khi có.
- Có thể dùng cronjob chạy hàng ngày để tự động kiểm tra và nhắc.


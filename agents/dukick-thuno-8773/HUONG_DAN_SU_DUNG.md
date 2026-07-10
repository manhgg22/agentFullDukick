# Dukick Agent Service — Hướng dẫn sử dụng

## Bot là gì

Bot Zalo hỗ trợ tra cứu lịch thanh toán theo hợp đồng và nhắc lịch chuyển khoản cho khách hàng Dukick.
Chạy tại port `8889`, nhận tin nhắn qua Zalo Bot Platform webhook.

---

## Cách dùng

### Hỏi tự do (AI trả lời)
Nhắn bất kỳ câu hỏi nào bằng tiếng Việt, bot sẽ trả lời tự nhiên.
> "Dukick làm gì?" / "Cho tôi biết về dự án HNS" / "Khi nào The One thanh toán?"

Nếu tin nhắn có tên project/khách hàng → bot tự load dữ liệu lịch thanh toán liên quan và trả lời cụ thể.

---

### Lệnh slash (admin)

| Lệnh | Tác dụng |
|---|---|
| `/help` | Xem danh sách lệnh |
| `/list overdue` | Liệt kê khoản chưa nhận xác nhận (đã qua ngày dự kiến) |
| `/list pending` | Liệt kê khoản sắp đến lịch |
| `/list all` | Toàn bộ 75 khoản |
| `/debts <tên>` | Tìm khoản theo tên khách/project |
| `/check` | Xem khoản của chính người nhắn (dùng Zalo ID tự động) |
| `/check <zalo_id>` | Xem khoản của bất kỳ Zalo ID |
| `/setid <zalo_id> <DEBT-IDs>` | Gán Zalo ID vào khoản (để bot nhắc tự động) |

#### Ví dụ

```
/debts The One
→ Hiện tất cả khoản của "The One" kèm ID, số tiền, ngày dự kiến, Zalo ID đã gán chưa

/debts HNS
→ Tìm tất cả khoản có chứa "HNS"

/list overdue
→ Gửi nhiều tin (mỗi tin 20 khoản) nếu danh sách dài

/setid 4a6f8b15bb40521e0b51 DEBT-0005,DEBT-0006,DEBT-0007
→ Gán Zalo ID vào 3 khoản của The One

/check 4a6f8b15bb40521e0b51
→ Tra cứu tên + toàn bộ khoản của người có Zalo ID đó
```

---

## Nhắc lịch tự động (Scheduler)

Script `scripts/reminder_scheduler.py` — chạy hàng ngày, tự gửi tin nhắn Zalo cho khách có khoản:
- Đã qua ngày dự kiến (chưa xác nhận)
- Sắp đến lịch trong vòng **3 ngày**

**Điều kiện**: khoản phải có `contact_phone` = Zalo user ID của khách.

Chạy thủ công:
```
C:/DukickAgent/venv/Scripts/python.exe agents/dukick-thuno-8773/scripts/reminder_scheduler.py
```

Hoặc cài Windows Task Scheduler chạy mỗi sáng 8h.

---

## Dữ liệu công nợ

File: `agents/dukick-thuno-8773/debt_data/debts.json`

| Field | Ý nghĩa |
|---|---|
| `id` | DEBT-0001 → DEBT-0075 |
| `client_name` | Tên khách hàng |
| `project` | Tên project / đợt thanh toán |
| `amount` | Số tiền (VND) |
| `due_date` | Ngày dự kiến thanh toán (YYYY-MM-DD) |
| `status` | `pending` / `overdue` / `paid` |
| `contact_phone` | **Zalo user ID** của khách (để nhắc tự động) |
| `reminder_count` | Số lần đã nhắc |

### Import lại từ Excel
Khi file `sheet_2.xlsx` có dữ liệu mới:
```
C:/DukickAgent/venv/Scripts/python.exe agents/dukick-thuno-8773/scripts/import_excel.py
```
Sẽ **ghi đè** toàn bộ debts.json — chạy xong thì gán lại Zalo ID nếu cần.

### Cập nhật trạng thái khoản đã thanh toán
Gọi API:
```
POST http://localhost:8889/webhook/debt/update
{"id": "DEBT-0005", "status": "paid", "notes": "Da chuyen 03/07"}
```

---

## Quy trình gán Zalo ID

1. Nhắn `/debts <tên khách>` → lấy danh sách DEBT-xxxx
2. Lấy Zalo user ID của khách (từ lịch sử chat Zalo OA)
3. Nhắn `/setid <zalo_id> <DEBT-xxxx,DEBT-xxxx>`
4. Scheduler sẽ tự nhắc khách đó vào hôm sau

---

## Khởi động / Restart bot

```powershell
# Kill server cũ (port 8889)
Stop-Process -Id <PID> -Force

# Start server mới
Start-Process -FilePath "C:/DukickAgent/venv/Scripts/python.exe" `
  -ArgumentList "C:/DukickAgent/agents/dukick-thuno-8773/scripts/webhook_server.py" `
  -WorkingDirectory "C:/DukickAgent/agents/dukick-thuno-8773" `
  -WindowStyle Minimized
```

Kiểm tra:
```
curl http://localhost:8889/health
→ {"status": "ok"}
```

---

## Giới hạn của bot

- ❌ Không tự xóa/giảm khoản, cam kết gia hạn
- ❌ Không gửi báo cáo tài chính chính thức
- ❌ Không hỗ trợ slash command suggestion như Telegram (Zalo không có tính năng này)
- ✅ Mọi điều chỉnh khoản → kế toán Dukick quyết định

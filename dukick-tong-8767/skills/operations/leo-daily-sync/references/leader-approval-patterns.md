# Leader Approval Patterns — Chị Leo

> Tài liệu kèm theo `leo-daily-sync` skill. Ghi lại các tình huống duyệt thực tế để agent PM học mẫu.
> Cập nhật: 04/06/2026

---

## Pattern A: Duyệt báo giá pitch

### Ví dụ 1 — MB Land (04/06/2026)
| Mục | Chi tiết |
|-----|----------|
| Khách | Anh Nghĩa — MB Land |
| Hình thức | Pitch chỉ chấm báo giá (không cần treatment) |
| Thị trường | Các bên bid 100–200tr |
| Khối lượng | 60 ảnh (nhiều bối cảnh) + 1 video |
| DuKick đề xuất | 250tr (1 ngày quay + 1 ngày chụp) |
| Phản ứng chị Leo | *"250M thì có cơ hội win ko? Giá dưới ko làm đc >> đánh giá job ko tiềm năng thì dừng luôn"* |
| Kết luận | Nếu 250tr không win được → dừng, không làm |

### Bài học
- Agent PM cần tự đánh giá "có win không" trước khi trình chị.
- Giá mình cao hơn top bid đáng kể → flag ngay, đừng chờ.
- Không được cố chấp theo thị trường nếu thị trường đang bid thấp.

### Flow quyết định
```
Nhận brief báo giá
    ↓
Đánh giá thị trường (bid range)
    ↓
Giá DuKick > top bid + không thể giảm khối lượng?
    → Dừng luôn (Pattern A-Stop)
    ↓ NO
Có thể giảm gói / match giá?
    → Trình chị xem xét giá mới
    ↓ NO
Giá đủ margin + khả năng win
    → Duyệt khoảng giá → giao PM chốt chi tiết
```

---

## Pattern B: Duyệt job sản xuất

### Checklist nhanh
1. Timeline có chậm không?
2. Budget có âm không?
3. Ekip có đủ không?
4. Nếu cả 3 OK → duyệt tiến hành
5. Nếu có rủi ro → yêu cầu plan B hoặc dừng

---

## Những điều chị Leo KHÔNG chấp nhận

| # | Sai lầm | Hậu quả |
|---|---------|---------|
| 1 | Deadline dồn cuối ngày để chị duyệt | Phải có buffer thời gian |
| 2 | Xin ý kiến dài dòng không có đề xuất | Bị bác, phải làm lại |
| 3 | Báo giá thấp rồi phát sinh chi phí sau | Mất uy tín + thâm hụt |

---

## Khi nào agent PM được phép duyệt sơ bộ thay chị

Điều kiện đủ:
- Job đã xuất hiện ít nhất 1 lần trong quá khứ với cùng pattern
- Chị Leo đã từng phản ứng theo cùng 1 hướng (thường là dừng hoặc OK)
- Không có biến số mới (khách mới, khối lượng khác, deadline khác)

Điều kiện cần:
- Vẫn phải ghi log vào vault: *"Duyệt sơ bộ theo pattern X, chờ chị confirm"*
- Nếu chị phản hồi khác lần sau → update pattern ngay

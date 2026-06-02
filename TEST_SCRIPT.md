# TEST SCRIPT — DuKick Agent System

## Cách test
Vào Discord server đã thêm bot, gõ các lệnh dưới đây vào kênh tương ứng.

## Bot Account (@dukick-pm)
Test 1: @dukick-pm tạo job mới Hanoi Six
→ Expected: Bot hỏi khách hàng, Account phụ trách, timeline, deadline, budget, deliverables, người liên quan

Test 2: @dukick-pm hôm nay job Hanoi Six cần làm gì?
→ Expected: Danh sách task, deadline, người phụ trách, rủi ro

Test 3: @dukick-pm job nào đang trễ deadline?
→ Expected: List job có rủi ro timeline

Test 4: @dukick-pm tổng kết cuối ngày
→ Expected: Task đã xong, chưa xong, rủi ro, việc ngày mai

## Bot Sales (@dukick-truyenthong)
Test 5: @dukick-truyenthong thêm lead mới Heineken
→ Expected: Bot hỏi ngành hàng, người liên hệ, chức vụ, nguồn lead, nhu cầu, budget, timeline, next step

Test 6: @dukick-truyenthong lead nào chưa follow-up quá 3 ngày?
→ Expected: List lead cần follow

Test 7: @dukick-truyenthong soạn email pitching cho Heineken
→ Expected: Draft email phù hợp

## Bot Creative (@dukick-pmcreative)
Test 8: @dukick-pmcreative tạo concept cho job May 10
→ Expected: Bot hỏi brief, key message, tone, reference, format, deadline

Test 9: @dukick-pmcreative có comment nào chưa xử lý không?
→ Expected: List comment pending

Test 10: @dukick-pmcreative gom reference cho job này
→ Expected: Cấu trúc reference theo nhóm

## Bot Finance (@dukick-neolab)
Test 11: @dukick-neolab tạo khoản chi freelancer Hateco 5 triệu
→ Expected: Hỏi người đề xuất, người duyệt, chứng từ, deadline thanh toán

Test 12: @dukick-neolab job nào chưa quyết toán?
→ Expected: List job pending settlement

Test 13: @dukick-neolab báo cáo tài chính tuần này
→ Expected: Tổng thu, tổng chi, công nợ nổi bật

## Bot Tổng (@dukick-tong)
Test 14: @dukick-tong báo cáo toàn cảnh hôm nay
→ Expected: Tổng hợp từ 4 bộ phận: job rủi ro, lead nóng, công nợ, comment pending, việc cần leader

Test 15: @dukick-tong có điểm nghẽn nào giữa các bộ phận không?
→ Expected: Phân tích cross-department bottlenecks

## Kiểm tra Obsidian auto-save
Sau khi gửi bất kỳ tin nhắn nào trong kênh Discord có bot:
→ Mở Obsidian → DuKick-{BộPhận} → Discord → YYYY-MM-DD.md
→ Expected: Tin nhắn xuất hiện với format "### HH:MM — @Username"

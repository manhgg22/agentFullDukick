# TEST SCRIPT — Dukick Agent System

## Cách test
Vào Discord server đã thêm bot, gõ các lệnh dưới đây vào kênh tương ứng.

## Bot Account (@Dukick-pm)
Test 1: @Dukick-pm tạo job mới Hanoi Six
→ Expected: Bot hỏi khách hàng, Account phụ trách, timeline, deadline, budget, deliverables, người liên quan

Test 2: @Dukick-pm hôm nay job Hanoi Six cần làm gì?
→ Expected: Danh sách task, deadline, người phụ trách, rủi ro

Test 3: @Dukick-pm job nào đang trễ deadline?
→ Expected: List job có rủi ro timeline

Test 4: @Dukick-pm tổng kết cuối ngày
→ Expected: Task đã xong, chưa xong, rủi ro, việc ngày mai

## Bot Sales (@Dukick-truyenthong)
Test 5: @Dukick-truyenthong thêm lead mới Heineken
→ Expected: Bot hỏi ngành hàng, người liên hệ, chức vụ, nguồn lead, nhu cầu, budget, timeline, next step

Test 6: @Dukick-truyenthong lead nào chưa follow-up quá 3 ngày?
→ Expected: List lead cần follow

Test 7: @Dukick-truyenthong soạn email pitching cho Heineken
→ Expected: Draft email phù hợp

## Bot Creative (@Dukick-pmcreative)
Test 8: @Dukick-pmcreative tạo concept cho job May 10
→ Expected: Bot hỏi brief, key message, tone, reference, format, deadline

Test 9: @Dukick-pmcreative có comment nào chưa xử lý không?
→ Expected: List comment pending

Test 10: @Dukick-pmcreative gom reference cho job này
→ Expected: Cấu trúc reference theo nhóm

## Bot Finance (@Dukick-neolab)
Test 11: @Dukick-neolab tạo khoản chi freelancer Hateco 5 triệu
→ Expected: Hỏi người đề xuất, người duyệt, chứng từ, deadline thanh toán

Test 12: @Dukick-neolab job nào chưa quyết toán?
→ Expected: List job pending settlement

Test 13: @Dukick-neolab báo cáo tài chính tuần này
→ Expected: Tổng thu, tổng chi, công nợ nổi bật

## Bot Tổng (@Dukick-tong)
Test 14: @Dukick-tong báo cáo toàn cảnh hôm nay
→ Expected: Tổng hợp từ 4 bộ phận: job rủi ro, lead nóng, công nợ, comment pending, việc cần leader

Test 15: @Dukick-tong có điểm nghẽn nào giữa các bộ phận không?
→ Expected: Phân tích cross-department bottlenecks

## Kiểm tra Obsidian auto-save
Sau khi gửi bất kỳ tin nhắn nào trong kênh Discord có bot:
→ Mở Obsidian → Dukick-{BộPhận} → Discord → YYYY-MM-DD.md
→ Expected: Tin nhắn xuất hiện với format "### HH:MM — @Username"

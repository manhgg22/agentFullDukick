---
name: leo-daily-sync
description: >
  Workflow điều phối công việc cần chị Leo duyệt/xử lý qua Discord.
  Agent Tổng ping định kỳ các kênh, gom reply về #agent-mẹ.
triggers:
  - Chị Leo cần nắm toàn bộ việc phải làm
  - Team cần đưa việc cho chị duyệt
  - Báo cáo tổng hợp cuối ngày cho leader
---

# 🔄 Leo Daily Sync — Workflow Gom Việc Cho Leader

## Mục tiêu
- Chị Leo không cần lướt từng kênh Discord
- Mọi việc cần chị → được gom về #agent-mẹ, ngắn gọn, có nguồn gốc rõ ràng

## Các kênh cần theo dõi
| Kênh | Bộ phận | Việc thường gặp |
|------|---------|----------------|
| #pm | Account | Duyệt timeline, budget, báo cáo dự án |
| #pm-creative | Creative | Duyệt brief, concept, version |
| #truyền-thông | Sales | Chốt lead, pitching, handoff |
| #tài-chính | Finance | Ký duyệt chi, công nợ, quyết toán |
| #pm-mkt | Marketing | Chiến dịch, content cần duyệt |
| #marketing | Marketing | Kế hoạch, báo cáo |
| #sx-quản-trị-team | Sản xuất | Lịch quay, booking, vật tư |
| #quản-lý-cấp-trung | Quản lý | Quyết định chiến lược, nhân sự |

## Quy trình hoạt động

### 1. Ping định kỳ (cronjob)
- **Sáng 9h** — Job ID: `24b5d0e0d2a1`
- **Trưa 14h** — Job ID: `3b1d1b6d4b61`
- **Tối 17h** — Job ID: `3a1acbfeaef3`

Nội dung ping:
```
👋 Team ơi!

Chị **Leo** đang cần nắm toàn bộ việc cần duyệt / chốt / nghe báo cáo.
Ai có việc cần chị, hãy reply ngay vào thread này hoặc @Agent Tổng.

Format reply:
• Tên job:
• Cần chị làm gì:
• Deadline:
• Mức độ khẩn: (bình thường / khẩn / gấp)

Không có việc → react ✅
```

### 2. Xử lý khi team reply
- **Reply trực tiếp** trong thread/cuộc trò chuyện đó để xác nhận đã ghi nhận
- **Copy nguyên văn** về #agent-mẹ theo format:
```
📥 [Từ #<kênh>, @<người> <HH:MM>]
• Tên job: ...
• Cần chị làm gì: ...
• Deadline: ...
• Mức độ khẩn: ...
```

### 3. Tổng hợp cho chị
- Cuối mỗi đợt ping → gom tất cả reply **có chứa `CẦN CHỊ LEO DUYỆT`** và đã được react like
- Bỏ qua tin nhắn thiếu format → không nhắc nhở, không gom vào báo cáo (team tự chịu trách nhiệm)
- Thành 1 bảng:
```
| # | Kênh | Người | Việc | Deadline | Khẩn |
```
- Đưa lên #agent-mẹ để chị xem 1 lần

### 4. Khi chị Leo công bố quy tắc / rule mới
- **Ghi nhận ngay** bằng cách lưu vào memory + cập nhật skill này
- **Tóm tắt lại** rule để team đồng thuận (ngắn gọn, dễ scan)
- **Thông báo** trong #agent-mẹ: *"Em đã cập nhật rule mới, mọi người check nhé"*
- **Không cần chị Leo duyệt lại** — đây là directive từ leader, agent tự ghi nhận và áp dụng

## Quy tắc tag chị Leo (BẮT BUỘC)
Kể từ 04/06/2026, mọi tin nhắn cần chị Leo xử lý **phải tuân thủ**:
1. **Tag @Leo🌷 + kèm câu: `CẦN CHỊ LEO DUYỆT`**
2. **Mọi người trong thread đều phải like (react ❤️/👍) tin nhắn đó**
3. Không làm đúng 2 điều trên → **coi như chị chưa nhận được**, agent sẽ không gom vào báo cáo

> ⚠️ **Lưu ý cho Agent Tổng:** Khi tổng hợp việc cần duyệt, chỉ lọc các tin nhắn có chứa cụm `"CẦN CHỊ LEO DUYỆT"` và đã được react. Các tin còn lại bỏ qua, không nhắc nhở — team tự chịu trách nhiệm tuân thủ format.

## Cách team sử dụng
1. Thấy việc cần chị Leo → **reply vào thread gốc** hoặc **@Agent Tổng**
2. **Bắt buộc viết thêm: `CẦN CHỊ LEO DUYỆT`**
3. **Bắt buộc react like** để chị xác nhận đã thấy
4. Cung cấp đủ 4 thông tin: Tên job / Cần chị làm gì / Deadline / Mức độ khẩn
5. Đính kèm file/link nếu cần chị xem

## Xử lý lỗi
- Nếu cronjob gửi kênh nào bị **403** → báo ngay trong #agent-mẹ để admin cấp quyền
- Nếu chị Leo ốm/nghỉ → cronjob vẫn chạy, team tự chủ, việc khẩn ping trực tiếp
  - **Agent vẫn gom việc** nhưng ghi rõ *"Chị Leo đang nghỉ ốm — việc này cần xử lý khi chị trở lại hoặc delegate cho người thay quyền"*
  - **Không gom việc khẩn** vào báo cáo chờ duyệt — việc khẩn phải được xử lý ngay, không để chờ
- Nếu cronjob gặp lỗi kênh #pm hoặc bất kỳ kênh nào không có quyền gửi → **thông báo ngay** để admin fix quyền bot
---
name: leo-daily-sync
description: >
  Workflow điều phối công việc cần chị Leo duyệt/xử lý qua Discord.
  Agent Tổng ping định kỳ các kênh, gom reply về #agent-mẹ.
triggers:
  - Chị Leo cần nắm toàn bộ việc phải làm
  - Team cần đưa việc cho chị duyệt
  - Báo cáo tổng hợp cuối ngày cho leader
  - Leader đã hẹn review/quyết định về policy, bảo mật, hoặc quy trình nhưng chưa chốt
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

### 2b. Nhắc chị Leo về quyết định / review chưa chốt
- Khi chị đã hẹn review một topic (bảo mật, phân quyền, policy) nhưng chưa chốt → gửi reminder ngắn gọn theo template `templates/reminder-security-review.md`
- Cấu trúc: Xác nhận lại topic → liệt kê tối đa 3 câu hỏi A/B → deadline → CTA
- Ví dụ đã dùng: nhắc review bảo mật DM agent + phân quyền Obsidian vault

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

## Phong cách báo cáo chị Leo yêu thích
- **Định dạng = tin nhắn Discord trực tiếp**, không đính kèm file Markdown phức tạp
- **Ngắn gọn, dễ scan** — bảng ngắn, bullet points, không dài dòng
- **Không giải thích nhiều** — đưa số liệu + kết luận, bỏ phần "tại sao em làm vậy"
- **Có mẫu điền sẵn** trong nội dung tin nhắn để team chỉ việc填 blank
- Ví dụ mẫu: `references/weekly-ai-cost-report-template.md`

> ⚠️ **Pitfall đã gặp:** Chị Leo đã chỉnh sửa lần 1: "ko cần quá phức tạp đâu, dễ hiểu dễ đọc bao quát là đc". Agent Tổng phải luôn ưu tiên format Discord-native, scan-friendly khi báo cáo cho leader.

## Cách team sử dụng
1. Thấy việc cần chị Leo → **reply vào thread gốc** hoặc **@Agent Tổng**
2. **Bắt buộc viết thêm: `CẦN CHỊ LEO DUYỆT`**
3. **Bắt buộc react like** để chị xác nhận đã thấy
4. Cung cấp đủ 4 thông tin: Tên job / Cần chị làm gì / Deadline / Mức độ khẩn
5. Đính kèm file/link nếu cần chị xem

## Tiêu chí duyệt sơ bộ của chị Leo (Pattern cho PM agent)

Khi chị Leo chỉ đạo *"quan sát cách chị duyệt >> update vault để sau này duyệt sơ bộ cho các bạn"*, agent PM phải áp dụng checklist này trước khi đưa việc lên chị.

### Tâm thế duyệt
- Không lãng phí thời gian — job không tiềm năng thì **dừng luôn**
- Giá phải đủ margin; dưới sàn thì **không làm**
- Câu hỏi đầu tiên: *"Giá này có cơ hội win không?"*
- Thích Yes/No hoặc "dừng luôn", không thích dài dòng

### Checklist 5 tiêu chí
| # | Tiêu chí | Câu hỏi | Ngưỡng |
|---|----------|---------|--------|
| 1 | Tiềm năng win | Khách thực sự cần mình? Đã có bên nào bid? | Nếu giá mình cao nhất trong chấm giá → đánh giá lại |
| 2 | Giá đủ làm | Bù đắp chi phí + margin tối thiểu? | Dưới giá sàn → **không làm** |
| 3 | Khối lượng khả thi | Số ảnh/video/bối cảnh thực hiện đúng hạn? | Quá lớn so với ngân sách → cảnh báo |
| 4 | Thời gian | Shoot + post kịp deadline? | Không nhận job cháy deadline nếu không có contingency |
| 5 | Loại job | Chỉ chấm giá hay cần treatment/proposal? | Chỉ chấm giá → nhanh gọn, không cần creative sâu |

### Pattern hành động
**Pattern A — Duyệt báo giá pitch**
1. Hỏi: *"Giá này có win không?"*
2. Nếu thị trường thấp hơn sàn → hỏi: "Có thể giảm khối lượng / gói dịch vụ để match không?"
3. Không match → **dừng luôn**
4. Có cơ hội → duyệt khoảng giá + giao PM chốt chi tiết

**Pattern B — Duyệt job sản xuất**
1. Kiểm tra timeline, budget, ekip
2. OK → duyệt tiến hành
3. Có rủi ro → yêu cầu plan B hoặc dừng

### Những điều chị Leo KHÔNG chấp nhận
- Deadline dồn cuối ngày để chị duyệt — phải có buffer
- Xin ý kiến dài dòng không có đề xuất cụ thể
- Báo giá thấp rồi phát sinh chi phí sau

Chi tiết và ví dụ thực tế: `references/leader-approval-patterns.md`

## Nhắc nhở cá nhân — 2 kiểu

Khi chị Leo hoặc leader giao việc cho **1 cá nhân/bộ phận cụ thể** và cần theo dõi đến khi xong, có 2 kiểu follow-up. Chọn đúng kiểu theo mức độ khẩn và tính chất công việc.

### Kiểu A — Escalating Reminder (Tăng độ nghiêm trọng)

Dùng khi: Việc **đang cháy**, cần phản hồi ngay lập tức, hoặc cá nhân đang ì ạch không trả lời.

| Điểm | Mô tả |
|------|-------|
| Đối tượng | 1 người cụ thể (tag Discord ID) |
| Tần suất | Mỗi 2 tiếng (hoặc theo yêu cầu) |
| Mức độ | Tăng dần mỗi lần nhắc (1→6) |
| Dừng | Khi người được nhắc reply `xong` hoặc `@Agent Tổng xong` |
| Deliver | Vào kênh leader đang chat (hoặc kênh chỉ định) |

### 6 mức độ nghiêm trọng

| Lần | Emoji | Nhãn | Ghi chú |
|-----|-------|------|---------|
| 1 | 📌 | Nhắc nhẹ nhàng | Vui lòng phản hồi khi có thể |
| 2 | ⏰ | Nhắc lại | Cần phản hồi để biết tiến độ |
| 3 | ⚠️ | Cần phản hồi | Việc chờ lâu hơn dự kiến |
| 4 | 🔴 | Khẩn cấp | Yêu cầu phản hồi ngay |
| 5 | 🚨 | Nghiêm trọng | BOD đang chờ, cần gấp |
| 6 | 💀 | Cực kỳ khẩn cấp | Đã qua 5 lần — phản hồi NGAY LẬP TỨC |

### Cách triển khai

1. **Tạo file theo dõi** trong vault Tong: `AgentMe-Reminder-Status.md`
   - Ghi số lần đã nhắc, trạng thái (Đang chạy / Đã xong), mức độ hiện tại
2. **Viết script Python** (`scripts/escalating-reminder.py`)
   - Đọc file theo dõi → tính lần nhắc tiếp theo → in ra message Discord → cập nhật file theo dõi
3. **Tạo cronjob `no_agent=True`** chạy mỗi 2 tiếng, script output đi thẳng vào Discord
4. **Cơ chế dừng**: Khi agent nhận reply chứa từ `xong` từ người được nhắc → sửa file theo dõi thành `Trạng thái: Đã xong` → cronjob tự silent exit

### Kiểu B — Periodic Reminder (Nhắc định kỳ, không leo thang)

Dùng khi: Công việc **có deadline rõ ràng**, đang tiến triển bình thường, không cần ép buộc ngay lập tức. Chỉ cần nhắc nhẹ nhàng để người làm không quên.

| Điểm | Mô tả |
|------|-------|
| Đối tượng | 1–2 người cụ thể (tag Discord ID) hoặc 1 bộ phận |
| Tần suất | Theo yêu cầu — ví dụ: mỗi 2 ngày một lần |
| Mức độ | Không leo thang — luôn giọng nhẹ nhàng, mang tính nhắc nhở |
| Dừng | Khi người được nhắc báo "xong" hoặc deadline đã qua |
| Deliver | Vào kênh leader đang chat (hoặc kênh chỉ định) |

#### Cách triển khai

1. **Tạo cronjob LLM-driven** (không dùng `no_agent=True`)  
   - Vì nội dung nhắc thay đổi theo ngữ cảnh (mention deadline, hỏi tiến độ), cần LLM soạn tin nhắn
2. **Prompt tự chứa đầy đủ context**:
   - Tên công việc
   - Người làm (tag Discord ID)
   - Deadline
   - Mục đích (để tuần sau công bố, v.v.)
   - Kênh gửi
3. **Không cần file theo dõi phức tạp** — agent tự kiểm tra trong vault xem công việc đã hoàn thành chưa (tìm file, check tiến độ) rồi quyết định nhắc hay dừng
4. **Ví dụ prompt mẫu**:
   ```
   Hỏi tiến độ công việc của @Duck Mẹn và @Hương Nguyễn:
   "Chị Leo giao việc: Quy trình & HDSD agent chuyên môn + agent cá nhân
   và Hướng dẫn phân quyền & bảo mật từng agent — deadline hết tuần này (28/06)
   để tuần sau công bố.
   @Duck Mẹn @Hương Nguyễn 2 em update tiến độ giúp chị nhé!"

   Nếu công việc đã hoàn thành từ lần follow-up trước → báo "✅ Công việc đã hoàn thành, dừng follow-up." và kết thúc.
   Nếu chưa xong → gửi tin nhắn follow-up như trên.
   ```

#### So sánh 2 kiểu

| Tiêu chí | Escalating (Kiểu A) | Periodic (Kiểu B) |
|----------|---------------------|-------------------|
| Mục đích | Ép buộc phản hồi ngay | Nhắc nhẹ, giữ tiến độ |
| Tần suất | Mỗi 2 tiếng | Mỗi 2 ngày (tùy chỉnh) |
| Mức độ | Tăng dần 1→6 | Không leo thang |
| `no_agent` | Có (script chạy thẳng) | Không (LLM soạn tin) |
| File theo dõi | Cần (`AgentMe-Reminder-Status.md`) | Không cần, agent tự check vault |
| Dùng khi | Việc cháy / cá nhân ì ạch | Việc có deadline, tiến triển bình thường |

> **Quy tắc chọn kiểu:** Nếu chị Leo nói "follow hỏi... mỗi 2 ngày cho tới khi xong" → đó là **Periodic Reminder (Kiểu B)**, không phải Escalating.

### Tài liệu tham khảo
- Script sẵn sàng chạy: `scripts/escalating-reminder.py`
- Hướng dẫn setup + cách dừng: `references/escalating-reminder-setup.md`

## 💰 Theo dõi chi tiêu & Nhắc nộp bill

Theo yêu cầu HR (chị Hương Nguyễn), khi có nhân sự xin duyệt chi phí và được duyệt + chuyển khoản thành công, Agent Tổng phải tự động nhắc người đó nộp bill thanh toán cho HR vào ngày hôm sau.

### Quy trình

1. **Ghi nhận:** Khi phát hiện tin nhắn xin duyệt chi trên Discord → ghi vào file tracking trong vault.
2. **Theo dõi trạng thái:**
   - ⏳ Chờ duyệt
   - ✅ Đã duyệt / Chờ CK
   - 💰 Đã CK / Chờ bill
3. **Nhắc bill:** Ngày hôm sau sau khi xác nhận CK thành công → tag người xin chi yêu cầu gửi bill.

### File tracking

File: `Theo-Doi-Chi-Tieu.md` trong vault `Dukick-Tong`.
Cấu trúc bảng 3 giai đoạn: Chờ duyệt | Đã duyệt/CK | Đã CK chờ bill.

### Format nhắc nộp bill

```
@<người xin chi> Khoản chi [mục đích] — [số tiền] đã được chuyển khoản.
Vui lòng gửi bill thanh toán cho chị Hương Nguyễn (HR) để lưu chứng từ nhé.
```

### Lưu ý

- Tin nhắn xin duyệt chi vẫn phải tuân thủ **quy tắc tag chị Leo** (tag + `CẦN CHỊ LEO DUYỆT` + like).
- Nếu chị Leo duyệt bằng cách reply `ok` / `ck rồi nhé` → agent cập nhật trạng thái sang "Đã duyệt".
- Nếu người xin chi hoặc HR báo `đã chuyển` / `ck thành công` → agent cập nhật sang "Đã CK" và lên lịch nhắc bill ngày hôm sau.

## Xử lý lỗi

### Lỗi gửi tin nhắn `Unknown platform: origin`

`send_message(action='send')` yêu cầu `target` phải là **tên kênh/thread từ `send_message(action='list')`**.

- ❌ Không dùng `target='origin'` — bị lỗi `"Unknown platform: origin"`.
- ✅ Luôn gọi `send_message(action='list')` trước, sau đó copy tên kênh/thread chính xác.
- Ví dụ đúng: `target="discord:🔥 DUKICK / #🧬neolab / chi tiêu / topic 1492791191362732062"`

### Cron database bị corrupt do BOM
Nếu `cronjob(action='list')` trả về lỗi `Unexpected UTF-8 BOM`:
1. Dùng Python đọc file `jobs.json` ở `C:\DukickAgent\Dukick-tong-8767\cron\` bằng mode `'rb'`
2. Kiểm tra 3 byte đầu: `b'\xef\xbb\xbf'` → đó là BOM
3. Ghi lại file bằng cách cắt bỏ 3 byte đầu: `content[3:]`
4. Không dùng `utf-8-sig` đọc rồi ghi thường — dễ tái phạm BOM
5. Chi tiết script: `references/cron-bom-fix.md`

### Job gửi kênh bị 403
- Báo ngay trong #agent-mẹ để admin cấp quyền
- Nếu chị Leo ốm/nghỉ → cronjob vẫn chạy, team tự chủ, việc khẩn ping trực tiếp
  - **Agent vẫn gom việc** nhưng ghi rõ *"Chị Leo đang nghỉ ốm — việc này cần xử lý khi chị trở lại hoặc delegate cho người thay quyền"*
  - **Không gom việc khẩn** vào báo cáo chờ duyệt — việc khẩn phải được xử lý ngay, không để chờ
- Nếu cronjob gặp lỗi kênh #pm hoặc bất kỳ kênh nào không có quyền gửi → **thông báo ngay** để admin fix quyền bot

### Escalating reminder chạy nhưng không thấy output
- `no_agent=True` jobs chạy script → output gửi về `deliver` target
- Nếu không thấy tin nhắn: kiểm tra script file có tồn tại trong `scripts/` không, quyền ghi `cron/output/` có bị lock không
- Trước khi tạo job mới, luôn `cronjob(action='run', job_id=...)` để test thử
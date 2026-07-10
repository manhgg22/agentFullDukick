# Periodic Reminder — Hướng dẫn triển khai

> Skill: `leo-daily-sync` | Kiểu B — Nhắc định kỳ, không leo thang

---

## Trường hợp dùng

Chị Leo giao việc cho 1–2 người, có deadline rõ ràng, cần theo dõi tiến độ đến khi xong. Không cần ép buộc ngay lập tức — chỉ cần nhắc nhẹ nhàng để người làm không quên.

**Ví dụ thực tế:**
> "@Duck Mẹn ơi phối hợp với Mạnh để làm cho chị: 1. Quy trình & HDSD agent chuyên môn & agent cá nhân 2. Hướng dẫn full về phân quyền & bảo mật từng agent. Hết tuần này cần xong để tuần tới công bố."
> 
> "follow hỏi @Duck Mẹn và @Hương Nguyễn mỗi 2 ngày cho tới khi xong thì thôi"

---

## Cách tạo cronjob

### Bước 1: Kiểm tra job đang chạy

```python
# Đảm bảo không trùng lặp với job cũ
cronjob(action='list')
```

Nếu đã có job follow-up cho cùng công việc → xoá hoặc update job cũ.

### Bước 2: Tạo cronjob LLM-driven

**KHÔNG dùng `no_agent=True`** — vì nội dung nhắc thay đổi theo ngữ cảnh, cần LLM soạn tin nhắn phù hợp.

```python
# Ví dụ: follow mỗi 2 ngày, bắt đầu từ ngày mai 9h sáng
cronjob(
    action='create',
    name='Follow-up HDSD Agent + Phân quyền/Bảo mật',
    schedule='0 9 */2 * *',   # 9:00 sáng, mỗi 2 ngày
    prompt="""Hỏi tiến độ công việc của @Duck Mẹn và @Hương Nguyễn:

\u0022Chị Leo giao việc: **Quy trình & HDSD agent chuyên môn + agent cá nhân**
và **Hướng dẫn phân quyền & bảo mật từng agent** — deadline hết tuần này (28/06)
để tuần sau công bố.

@Duck Mẹn @Hương Nguyễn 2 em update tiến độ giúp chị nhé!\u0022

Nếu công việc đã hoàn thành từ lần follow-up trước → báo 
\u0022✅ Công việc đã hoàn thành, dừng follow-up.\u0022 và kết thúc.
Nếu chưa xong → gửi tin nhắn follow-up như trên.""",
    deliver='origin'   # gửi về channel đang chat
)
```

### Bước 3: Ghi nhận vào vault

Tạo file theo dõi trong `Dukick-Tong/Công việc/` để có nguồn gốc rõ ràng:

```markdown
# Công việc: [Tên công việc]
**Người giao việc:** Leo🌷 (CEO)
**Người thực hiện:** [Tên người/bộ phận]
**Deadline:** [date]
**Mục đích:** [để tuần sau công bố / v.v.]

## Tiến độ cập nhật
| Ngày | Cập nhật | Người cập nhật |
|------|----------|----------------|
| [date] | Giao việc | Agent Tổng |

## Follow-up
- **Lịch follow:** Mỗi [N] ngày một lần
- **Kênh follow:** #[kênh]
- **Người cần hỏi:** [tag Discord]
```

---

## Prompt mẫu đa năng

Khi cần tạo periodic reminder cho công việc khác, thay thế các placeholder:

```
Hỏi tiến độ công việc của {{NGƯỜI_LÀM}}:
"Chị Leo giao việc: {{TÊN_CÔNG_VIỆC}} — deadline {{DEADLINE}} để {{MỤC_ĐÍCH}}.

{{TAG_DISCORD}} update tiến độ giúp chị nhé!"

Nếu công việc đã hoàn thành từ lần follow-up trước → báo 
"✅ Công việc đã hoàn thành, dừng follow-up." và kết thúc.
Nếu chưa xong → gửi tin nhắn follow-up như trên.
```

---

## Khác biệt với Escalating Reminder

| | Periodic (Kiểu B) | Escalating (Kiểu A) |
|---|---|---|
| Mục đích | Nhắc nhẹ, giữ tiến độ | Ép buộc phản hồi ngay |
| Tần suất | Mỗi 2–3 ngày | Mỗi 2 tiếng |
| `no_agent` | Không | Có |
| File theo dõi | Không cần | Cần (`AgentMe-Reminder-Status.md`) |
| Dừng khi | Báo xong hoặc deadline qua | Reply chứa `xong` |

---

## Lưu ý

1. **Prompt phải tự chứa đầy đủ context** — cronjob chạy trong session riêng, không nhớ chat history. Nếu prompt thiếu deadline hoặc tên người làm → agent không biết hỏi ai.
2. **Không dùng `no_agent=True`** cho periodic reminder — nội dung nhắc cần LLM để soạn phù hợp ngữ cảnh, không phải script cố định.
3. **Deliver='origin'** → tin nhắn gửi về channel đang chat. Nếu muốn gửi sang channel khác → dùng `discord:#channel-name`.
4. **Khi công việc hoàn thành** → xoá hoặc pause cronjob để không spam. Có thể dùng `cronjob(action='remove', job_id=...)`.

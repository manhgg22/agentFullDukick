---
name: token-cost-signature
version: 1.0
category: operations
description: Auto-append token usage estimate and cost to every agent response.
---

# Token & Cost Signature

## Mục tiêu
Mọi response từ Agent Tổng phải kèm ước lượng token + chi phí ở cuối tin nhắn, format ngắn gọn.

## Quy tắc
1. **Luôn append** vào cuối mỗi response (trừ khi user nói "đừng kèm")
2. **Format:**
   ```
   —
   💬 ~{input_tokens}t in / ~{output_tokens}t out | 💰 ~${cost} | model: {model_name}
   ```
3. **Công thức ước lượng:**
   - Tiếng Việt: ~2.5 chars/token (modern tokenizer)
   - Tiếng Anh: ~4 chars/token
   - Input = độ dài toàn bộ context (system + memory + tools + user msg)
   - Output = độ dài response em vừa viết
4. **Giá tham khảo** (OpenAI API → kimi-k2.6):
   - Input: ~$0.005 / 1K tokens
   - Output: ~$0.015 / 1K tokens
   - Tổng cost = (input × 0.005 + output × 0.015) / 1000
5. **Làm tròn:** tokens đến hàng chục, cost đến 2 chữ số thập phân (cent)
6. **Không tính:** image gen, tool calls phức tạp (chỉ ước lượng text)

## Ví dụ
```
—
💬 ~420t in / ~180t out | 💰 ~$0.005 | model: kimi-k2.6
```

## Lưu ý
- Đây là ước lượng (estimate), không phải số thực từ API
- Hermes không expose token usage real-time nên dùng heuristic
- Nếu context >10K tokens, thêm cảnh báo: ⚠️ context cao
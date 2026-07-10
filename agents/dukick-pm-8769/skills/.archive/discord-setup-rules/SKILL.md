---
name: discord-setup-rules
title: Quy tắc Setup Discord Server
description: Quy trình setup Discord server cho dự án/khách hàng tại DUKICK
version: 1.0
created: 2026-06-25
---

# Quy tắc Setup Discord Server (DUKICK)

> Áp dụng cho: Các member khi lập server Discord mới cho dự án / khách hàng

## Bước 1: Tạo Role Admin
- Tạo role **Admin** ngay sau khi lập server
- Gán **tất cả các quyền** (permissions) cho role Admin
- **TRỪ dòng quyền cuối cùng** — quyền này chỉ dành cho Owner

## Bước 2: Tự add bản thân làm Admin
- Tự assign role Admin cho chính mình

## Bước 3: Add Role Admin vào các kênh Private
- Kiểm tra tất cả **kênh private** (Private Channels / Category permissions)
- **Add role Admin vào permission của từng kênh private** trước khi chuyển owner
- Đảm bảo Admin có quyền truy cập đầy đủ các kênh quan trọng

## Bước 4: Chuyển Ownership
- Sau cùng: **Move quyền Owner sang cho chị Leo🌷**
- Đảm bảo chị Leo🌷 nhận được ownership trước khi bàn giao server

## Lưu ý quan trọng
- Không để quyền Owner ở account cá nhân lâu dài
- Owner cuối cùng luôn là chị Leo🌷 để đảm bảo quản lý tập trung
- Kiểm tra lại permission sau khi setup xong

## IV. Discord Automation — Cronjob & Thread Messaging

### Target thread bằng send_message
Khi gửi tin nhắn vào thread trong kênh Discord, dùng format:
```
discord:<chat_id>:<thread_id>
```

Ví dụ thực tế tại DUKICK:
- Thread Thái: `discord:1093083512837521448:1407966179758182447`
- Thread Huyền: `discord:1093083512837521448:1511955929615040573`
- Thread Hoàng: `discord:1093083512837521448:1349587719424180294`

### Cronjob nhắc việc qua Discord
- Tạo cronjob với `enabled_toolsets: ["discord"]`
- Prompt nên ghi rõ target thread cho từng người để agent tự gửi tin nhắn
- Khi có thread mới hoặc thay đổi thread ID → update lại prompt trong cronjob ngay
- Luôn test gửi tin nhắn thủ công (`send_message`) trước khi để cronjob chạy tự động, để xác nhận target đúng và bot có quyền gửi

## Cách hỏi agent pm về sales & account
- Từng PM hãy vào thread riêng của mình trong kênh #pm-dukick để hỏi agent pm
- Có thể hỏi triệt để các định hướng, mẹo, chiêu thức về sales và account
- Agent pm đã được cập nhật thông tin chiến lược mới nhất từ chị Leo🌷

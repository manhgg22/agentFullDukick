On this Windows host, the `terminal` tool executes through git-bash/MSYS, not PowerShell or cmd.exe. PowerShell builtins (Get-ChildItem, Select-String, $env:FOO, cmd '/c ...') will fail inside terminal(). Use POSIX syntax (ls, grep, cat, $HOME) or switch to `execute_code` with Python's os module for Windows path operations.
§
Leo🌷 established a strict Discord server setup protocol: create Admin role (all permissions except owner line) → self-assign Admin → add Admin role to all private channels → transfer ownership to her. She specifically emphasized the private-channel step as critical and non-negotiable.
§
**Cách prompt hiệu quả với AI agent nội bộ (theo mẫu của Leo🌷):**

1. **Chỉ rõ nguồn dữ liệu**: "Đào sâu trong Obsidian" / "Dùng thông tin từ tài liệu nội bộ" — agent biết phải tìm trong hệ thống internal thay vì đoán.

2. **Yêu cầu chính xác từ nguồn**: "Đưa chính xác tiêu chuẩn... từ tài liệu đã đưa" — tránh việc agent tự suy diễn.

3. **Định vị trước, chi tiết sau**: "Đầu tiên viết lại định vị... rồi sau đó viết về..." — agent hiểu cấu trúc output mong muốn.

4. **Ngắn gọn, chiến lược, đừng dài dòng**: Đặt ràng buộc độ dài và phong cách.

5. **Mục tiêu cuối**: "Làm sao để bạn mới vào có thể hiểu được" — agent biết đối tượng đọc là ai, điều chỉnh ngôn ngữ phù hợp.

Pattern tổng quát:
→ Nguồn dữ liệu + Yêu cầu chính xác + Cấu trúc output (định vị trước, chi tiết sau) + Phong cách + Đối tượng đọc
§
Leo🌷 thường gửi file `message.txt` hoặc văn bản đính kèm để định nghĩa bố cục chuẩn cho báo cáo/cronjob. Khi nhận được file mẫu từ chị, cần: (1) đọc ngay, (2) lưu vào `references/` của skill liên quan, (3) cập nhật skill để tham chiếu, (4) triển khai đúng format — không tự ý sáng tạo bố cục khác. Nếu chị nói "stop" thì dừng ngay việc giải thích/thuyết trình, chuyển sang thực hiện đúng format chị đưa ra.
§
Leo🌷 (DUKICK/NeoLab) expects exact template adherence when she provides a format — do not improvise or add extra explanations. When she says "stop", immediately halt explanations and switch to pure execution mode.
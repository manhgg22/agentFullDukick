---
name: creative-workspace-tools
description: Bộ công cụ đầy đủ cho Creative PM — Canva, Google Drive, Google Docs, Google Sheets, tạo/đọc ảnh, tạo/đọc PDF, upload & chia sẻ file. Sử dụng khi cần tạo nội dung, quản lý tài liệu, hoặc xuất file cho khách hàng Hateco/Dukick.
category: productivity
---

# Creative Workspace Tools

Bộ công cụ đa năng cho PM Creative để làm việc với tài liệu, hình ảnh, và nội dung cho khách hàng.

---

## 1. GOOGLE DRIVE (Upload & Share)

**Sẵn có:** `shared/upload_to_drive.py`, `shared/drive_config.py`

### Quick Upload
```python
import sys
sys.path.insert(0, r"C:\DuKickAgent\agents\dukick-pmcreative-8770\shared")
from upload_to_drive import upload_file
from drive_config import get_folder_id

folder_id = get_folder_id("dukick-pmcreative-8770")
result = upload_file(
    r"C:\path\to\file.docx",
    folder_id=folder_id,
    convert=True,      # .docx → Google Docs, .xlsx → Sheets
    make_public=True   # Link chia sẻ anyone-can-edit
)
print(result["webViewLink"])
```

### Supported Conversions
| File | Converts To |
|------|-------------|
| `.docx` | Google Docs |
| `.xlsx` | Google Sheets |
| `.pptx` | Google Slides |
| `.pdf` | PDF (giữ nguyên) |

**⚠️ Pitfall:** Markdown `.md` phải convert sang `.docx` trước khi upload. Dùng `python-docx` hoặc `pandoc`.

---

## 2. GOOGLE DOCS (Create & Edit)

**Sẵn có:** `shared/docs_ops.py`

```python
import sys
sys.path.insert(0, r"C:\DuKickAgent\agents\dukick-pmcreative-8770\shared")
from docs_ops import create_doc, append_text, read_doc, insert_heading, replace_text

# Tạo doc mới
doc = create_doc("Tên tài liệu")
doc_id = doc["documentId"]

# Thêm nội dung
append_text(doc_id, "Nội dung đoạn văn.\n")
insert_heading(doc_id, "Tiêu đề chương", heading_level=1)

# Đọc doc từ link
# Lấy ID từ link: https://docs.google.com/document/d/ID/edit
doc_data = read_doc("DOC_ID_HERE")
```

---

## 3. GOOGLE SHEETS (Create & Edit)

**Sẵn có:** `shared/sheets_ops.py`

```python
import sys
sys.path.insert(0, r"C:\DuKickAgent\agents\dukick-pmcreative-8770\shared")
from sheets_ops import create_sheet, write_range, read_range, append_rows, clear_range

# Tạo sheet mới
sheet = create_sheet("Bảng tính dự án")
sheet_id = sheet["spreadsheetId"]

# Ghi dữ liệu
write_range(sheet_id, "Sheet1!A1:C3", [
    ["Cột A", "Cột B", "Cột C"],
    ["1", "2", "3"],
    ["4", "5", "6"]
])

# Đọc dữ liệu
data = read_range(sheet_id, "Sheet1!A1:C10")
print(data.get("values", []))
```

---

## 4. TẠO ẢNH (Image Generation)

**Tool:** `image_generate`

Dùng khi cần tạo moodboard, concept visual, hoặc reference hình ảnh cho khách hàng.

```python
# Trong execute_code không dùng được — gọi trực tiếp tool image_generate
# Ví dụ prompt cho TVC Intercentral:
"Luxury modern lobby with floating golden picture frames containing 
Singapore skyline and Hanoi old quarter scenes, cinematic lighting, 
architectural photography style, warm and cool color contrast, 
Unreal Engine render quality"
```

**Aspect ratios:** `landscape` (16:9), `portrait` (9:16), `square` (1:1)

---

## 5. ĐỌC ẢNH (Vision / OCR)

**Tool:** `vision_analyze`

Dùng khi cần phân tích ảnh concept, moodboard, hoặc brief thiết kế từ khách hàng.

```
vision_analyze(image_url="https://...", question="Describe the color palette and composition")
```

**Hoặc** đọc ảnh local:
```
vision_analyze(image_url="C:\path\to\image.jpg", question="What architecture style is this?")
```

---

## 6. PDF (Read & Create)

### Đọc PDF
**Tool:** `mcp_markitdown_convert_to_markdown` (hoặc `read_file` cho text-based PDF)

```python
from hermes_tools import mcp_markitdown_convert_to_markdown
result = mcp_markitdown_convert_to_markdown(source=r"C:\path\to\file.pdf")
print(result["content"])
```

### Tạo PDF
Chưa có tool native. Đề xuất workflow:
1. Viết nội dung → `.docx` (dùng `python-docx`)
2. Upload lên Drive → convert sang Google Docs
3. Từ Google Docs xuất PDF (hoặc dùng LibreOffice headless convert)

**Alternative — Convert DOCX → PDF local:**
```bash
# Nếu có LibreOffice installed
libreoffice --headless --convert-to pdf file.docx --outdir /path/
```

---

## 7. CANVA

**⚠️ Hiện tại chưa có API integration.** Canva không cung cấp public API cho việc tạo design tự động.

**Workarounds:**
1. Tạo nội dung text/hình → upload lên Drive → gửi link cho designer mở trong Canva
2. Dùng Canva Magic Write trực tiếp (cần designer thao tác tay)
3. Export từ Canva template → đọc file PDF/PPTX bằng MarkItDown

**Nếu cần automation Canva:** Cân nhắc dùng Figma API (có public API) hoặc Adobe Express API.

---

## 8. WORKFLOW TÍCH HỢP (Ví dụ thực tế)

### Workflow: Tạo Treatment gửi khách hàng Hateco
```
1. Tạo nội dung bằng python-docx → file .docx
2. upload_file() → Google Docs trên Drive DUKICK
3. Nếu cần bảng dự toán: create_sheet() + write_range() → Google Sheets
4. Nếu cần ảnh minh họa: image_generate() → lưu local → upload_file() lên Drive
5. Gửi link Google Docs + Sheets cho khách hàng
```

---

## References
- `shared/gauth.py` — OAuth auto-refresh
- `shared/drive_config.py` — Agent folder mapping
- `shared/upload_to_drive.py` — Upload + convert + public link
- `shared/docs_ops.py` — Google Docs CRUD
- `shared/sheets_ops.py` — Google Sheets CRUD

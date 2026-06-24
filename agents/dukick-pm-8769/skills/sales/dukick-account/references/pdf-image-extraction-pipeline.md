# PDF Image-Based Extraction Pipeline

When a PDF brief (from Canva, InDesign, or scanned) contains no extractable text, use this pipeline to convert pages to images and read them via vision.

## Steps

1. **Try text extraction first**
   ```python
   import pdfplumber
   with pdfplumber.open(pdf_path) as pdf:
       for page in pdf.pages:
           text = page.extract_text()
   ```
   If all pages return empty → PDF is image-based.

2. **Extract pages as PNG via PyMuPDF**
   ```python
   import fitz, os
   doc = fitz.open(pdf_path)
   out_dir = "./pdf_pages"
   os.makedirs(out_dir, exist_ok=True)
   for i, page in enumerate(doc):
       pix = page.get_pixmap(dpi=200)
       pix.save(os.path.join(out_dir, f"page_{i+1:02d}.png"))
   doc.close()
   ```

3. **Batch pages for vision analysis**
   - Combine 4–5 consecutive pages vertically using PIL into one image.
   - Send to `vision_analyze` with a detailed prompt asking for text extraction + structured summary.
   - Process in batches to stay within token/context limits.

4. **Aggregate results**
   - Compile text from all batches into a single markdown analysis.

## Pitfalls

- `pdfplumber` text extraction fails silently on designer PDFs (all pages empty).
- Do NOT try `curl` / `requests` on Canva share links — they return HTML shell requiring login.
- Always ask the user to download the PDF or share screenshots if links don't work.
- High-DPI PNGs (300+) can be too large for vision; 200 DPI is a good balance.

## Example: Batch combination
```python
from PIL import Image
pages = ["page_01.png", "page_02.png", "page_03.png", "page_04.png"]
ims = [Image.open(p) for p in pages]
max_w = max(im.width for im in ims)
total_h = sum(im.height for im in ims)
combined = Image.new('RGB', (max_w, total_h), (255,255,255))
y = 0
for im in ims:
    combined.paste(im, (0, y))
    y += im.height
combined.save("batch_1_4.png")
```

# Canva Brief Link Pitfalls

## Symptom
- `requests.get("https://canva.link/XXXXX")` returns `status 200` but HTML content is a shell/loader (~850KB minified JS/CSS).
- No meaningful text content after HTML stripping — only CSS variables, JS bundles, and metadata.

## Root Cause
Canva share links redirect to an authenticated editor view (`/design/.../edit`). The actual design content is loaded client-side via JavaScript and requires:
1. A logged-in Canva session (cookies)
2. Browser execution environment to render the canvas

## Verification
Fetch the page and look for these tells:
- Page title includes "Canva" but no visible design text in raw HTML
- `<script>` tags containing large minified bundles (500KB+)
- No readable paragraph text or bullet lists outside metadata

## Workarounds (in preferred order)
1. **Ask the user to export as PDF / PNG / JPEG** from Canva → send file directly. Use `vision_analyze` on the image or `read_file` on the PDF.
2. **Ask the user to copy-paste the brief text** directly into chat.
3. **Screenshot per page** → use `vision_analyze` to extract all text/imagery.
4. **If user cannot export:** Proceed with a template proposal and clearly state "brief content not accessible yet" — do not fabricate brand details.

## Do NOT
- Spend more than one attempt parsing shell HTML. It will not work.
- Try to execute the JavaScript in `execute_code` — Canva apps depend heavily on browser APIs and runtime auth.
- Assume the link is broken or dead. HTTP 200 with ~850KB is the expected response for a gated design.

# Extracting Google Docs That Require Login

When a user provides a Google Docs edit/view link that requires authentication, you cannot open it directly. Use the `r.jina.ai` summarizer as a text extraction proxy.

## Fallback URL pattern
Replace the original URL with:

```
https://r.jina.ai/http://<full-google-doc-url>
```

Example:
- Original: `https://docs.google.com/document/d/1p0galjhBFUwZgtaybXcwmrtQMg98otXi/edit`
- Fallback: `https://r.jina.ai/http://docs.google.com/document/d/1p0galjhBFUwZgtaybXcwmrtQMg98otXi/edit`

## Tool
```python
import requests
url = "https://r.jina.ai/http://docs.google.com/document/d/DOC_ID/edit"
r = requests.get(url, timeout=20)
text = r.text
```

## Limitations
- JS-heavy formatting is lost; you get plain Markdown-ish text.
- If the doc is truly private (no public link), `r.jina.ai` may still return empty or truncated results. Use `https://r.jina.ai/http://` not `https://r.jina.ai/http+s://`.
- Always verify extracted text is not just UI chrome (e.g., generic Google Docs menus), and search for meaningful content like bullet points or headings.

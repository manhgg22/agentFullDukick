---
name: meeting-recap
description: |
  Handle audio/video meeting uploads: extract audio → transcribe → LLM summary →
  present in chat for user approval → save to Drive only after explicit "OK".
  Supports OpenAI Whisper API (fast) and local faster-whisper (offline).
trigger: |
  User uploads an audio or video file and asks for transcript, recap, meeting notes,
  or ghi chép cuộc họp. Also applies when user says "tóm tắt cuộc họp", "recap",
  "ghi âm này", "meeting này", etc.
---

# Meeting Recap Workflow

## Overview
Pipeline: **Upload → Extract Audio → Transcribe → LLM Recap → Chat Approval → Drive Save**

## 1. Receiving Files
Accept any audio/video format: `.mp3`, `.wav`, `.ogg`, `.oga`, `.m4a`, `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`.

If video: extract audio via ffmpeg → `.mp3` (16kHz mono, 32kbps):
```bash
ffmpeg -y -i input.mp4 -vn -ar 16000 -ac 1 -b:a 32k output.mp3
```

## 2. Transcription Options

| Tool | Speed | Quality tiếng Việt | Requires API key | Offline |
|------|-------|-------------------|------------------|---------|
| **Groq Whisper API** (whisper-large-v3) | ~10-20s / 10 phút | Tốt | ✅ GROQ_API_KEY | ❌ |
| **OpenAI Whisper API** | ~30-60s / 10 phút | Tốt | ✅ OPENAI_API_KEY | ❌ |
| `faster-whisper` **small** (CPU) | ~2-3 phút / 10 phút | Tốt | ❌ | ✅ |
| `faster-whisper` base (CPU) | ~3-5 phút / 10 phút | **GARBAGE cho tiếng Việt** | ❌ | ✅ |

**Default:** Groq/OpenAI Whisper API nếu key sẵn. Fallback local `small` nếu không.

⚠️ **CRITICAL:** `faster-whisper` `base` model cho tiếng Việt ra transcript vô nghĩa (gibberish). Luôn dùng `small` hoặc lớn hơn cho tiếng Việt.

### API Key Caveat
API key cho LLM inference (e.g. OpenRouter) **không phải** OpenAI API key. Nếu key hiện tại trả 401 từ `api.openai.com`, fallback ngay sang local model — đừng retry liên tục.

### Groq Whisper API call
```python
import requests, os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def transcribe_groq(audio_path):
    with open(audio_path, "rb") as f:
        resp = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            files={"file": (os.path.basename(audio_path), f, "audio/mpeg")},
            data={"model": "whisper-large-v3", "language": "vi", "response_format": "text"},
            timeout=300,
        )
    resp.raise_for_status()
    return resp.text.strip()
```

### OpenAI Whisper API call
```python
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

def transcribe_openai(audio_path):
    with open(audio_path, "rb") as f:
        resp = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": (os.path.basename(audio_path), f, "audio/mpeg")},
            data={"model": "whisper-1", "language": "vi", "response_format": "text"},
            timeout=300,
        )
    resp.raise_for_status()
    return resp.text.strip()
```

### faster-whisper local (fallback)
```python
from faster_whisper import WhisperModel
# ⚠️ Dùng "small" cho tiếng Việt — "base" là vô nghĩa
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_path, beam_size=5, language="vi")
text = " ".join([seg.text for seg in segments])
```

## 3. Generate Recap via LLM
Gửi transcript lên LLM (gpt-4o-mini hoặc model hiện tại) với prompt:

```
Bạn là trợ lý ghi chép cuộc họp chuyên nghiệp. Hãy phân tích transcript dưới đây
và tóm tắt thành bản recap bằng tiếng Việt theo cấu trúc:

1. Tóm tắt chung (2-3 câu)
2. Nội dung chính (bullet points các chủ đề đã bàn)
3. Quyết định / Thống nhất (nếu có)
4. Action items — bảng: | Người phụ trách | Việc cần làm | Deadline |

Lưu ý: Nếu không rõ người phụ trách hoặc deadline thì để dấu "?".
Giữ giọng văn súc tích, dễ đọc.
```

## 4. ⚠️ CRITICAL: Approval Gate — NEVER Auto-Save

**User preference (enforced):**
- **Gửi recap trong chat TRƯỚC** → user đọc & duyệt
- **Chỉ lưu Drive khi user nói "OK", "duyệt", "lưu", "được", "save"**
- **KHÔNG BAO GIỜ** tự động upload lên Drive trước khi user phản hồi

### Quy trình đúng:
```
User gửi file → Agent: transcript + recap trong chat
                          ↓
                    User: "OK lưu" hoặc "duyệt"
                          ↓
                    Agent: upload lên Drive + trả link
```

### Quy trình sai (ĐÃ BỊ CORRECT):
```
User gửi file → Agent: transcript + recap + TỰ ĐỘNG SAVE DRIVE ❌
```

## 5. Drive Save (Post-Approval)

Khi user approved, lưu 2 file:
1. `{base}_transcript.txt` — transcript đầy đủ
2. `{base}_recap.md` — recap đã duyệt

Upload vào đúng folder agent trên Drive (lấy từ `drive_config.py`).
Mặc định public + quyền edit (`make_public=True`).

## 6. Script Reference
See `scripts/meeting_recap.py` — full pipeline script dùng OpenAI Whisper API.

## 7. Pitfalls
| Pitfall | Fix |
|---------|-----|
| Tự động lưu Drive trước khi user duyệt | **Luôn đợi explicit approval** |
| Dùng faster-whisper `base` cho tiếng Việt | **Luôn dùng `small` hoặc API** — base ra gibberish |
| API key của LLM provider (OpenRouter) không chạy Whisper API | Key khác nhau! Fallback local ngay khi 401 |
| `write_file` với tiếng Việt bị corrupt (invisible chars/BOM) | Dùng `execute_code` Python raw string để ghi file .py |
| Quên convert video → audio trước khi transcribe | Luôn check extension, ffmpeg extract nếu video |
| Transcript quá dài gây context overflow | Cắt transcript thành chunks nếu >4000 tokens khi gửi LLM |

## 8. Templates
- `templates/meeting_recap_prompt.md` — Prompt template gửi LLM
- `templates/meeting_recap_approval_msg.md` — Message template gửi user khi xong recap (chờ duyệt)

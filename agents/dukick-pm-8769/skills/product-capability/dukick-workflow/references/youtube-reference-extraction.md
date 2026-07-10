# Trích xuất & Phân tích YouTube Reference

## When to Use
- Khách gửi link YouTube làm reference cho TVC/photo/shoot creative direction.
- Cần trích xuất transcript, mô tả visual, tone, pacing để viết treatment.

## 3-Tier Extraction Pipeline

### Tier 1: youtube-transcript-api (Best)
```bash
pip install youtube-transcript-api
```
```python
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript("VIDEO_ID", languages=['en', 'vi'])
full_text = " ".join([seg['text'] for seg in transcript])
```
**Pros:** Đầy đủ text, timestamp. **Cons:** Có video bị disable transcript (rare).

### Tier 2: r.jina.ai Proxy
```bash
curl -sL "https://r.jina.ai/http://www.youtube.com/watch?v=VIDEO_ID"
```
**Pros:** Không cần install gì. **Cons:** Trả về HTML shell nếu YouTube block. Thử thêm `si` param từ share link.

### Tier 3: textise.iitty.com
```bash
curl -sL "https://r.jina.ai/http://textise.iitty.com"
```
**Fallback** khi jina.ai return 403.

## What to Extract & Document

| Field | Why it matters |
|-------|---------------|
| **Title + Channel** | Context về who made it, what level |
| **Duration** | Pacing expectation |
| **Visual Style Notes** | Bright/dark, staged/candid, warm/cool grade |
| **Key Scenes** | Hero shots, transitions, signature moments |
| **Music Style** | Genre, instrumentation, emotional arc |
| **Color Palette** | Dominant tones, grade style |
| **Camera Movement** | Steadicam, handheld, static, gimbal |
| **Pacing Structure** | Slow intro → build → peak → resolve |
| **VO/Narration** | Tone, language, presence/absence |
| **What to Avoid** | Staged, corporate, generic — note what feels "off" |

## Pattern Recognition (International School TVC)

Sau khi phân tích >10 reference trường học quốc tế VN, pattern chung:

1. **Journey Narrative** — 1-2 nhân vật qua các cấp học → kết nối cảm xúc
2. **Campus Showcase** — Toàn cảnh facility → establish prestige
3. **Student Voices** — Học sinh nói về experience → authentic
4. **Warm Palette** — Vàng nắng, xanh lá, trắng sáng → approachable premium
5. **Dynamic Movement** — Walking, running, interacting → energetic
6. **Uplifting Music** — Piano → strings → crescendo → emotional build

## Template: Reference Analysis Output

```
## Ref: [Title] ([Channel])
**URL:** [link]
**Duration:** [X]s

### Visual
- Style: [cinematic / documentary / staged]
- Color: [warm / cool / neutral / saturated]
- Camera: [steadicam / handheld / static / gimbal]
- Key shots: [list 3-5]

### Audio
- Music: [genre, instruments, arc]
- VO: [yes/no, tone, language]
- Sound design: [notable]

### Pacing
- Structure: [slow intro → build → peak → resolve]
- BPM/Energy: [low/medium/high]

### What Works
- [point 1]
- [point 2]

### What to Avoid
- [point 1]

### Applicability to [Client]
- [How this ref maps to client's brand pillars/brief]
```

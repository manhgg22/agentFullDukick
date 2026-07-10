---
name: audio-processing
description: Transcribe, convert, and segment audio files using OpenAI Whisper and FFmpeg. Covers long-form transcription workflows, Vietnamese-language audio, and timeout-safe batch processing on CPU.
category: creative
---

# Audio Processing

Transcribe, convert, and segment audio recordings into readable text. Optimized for long voice memos, meeting recordings, and interview files where built-in transcription tools may fail or time out.

## When to Activate

- User asks to "transcribe", "nghe file ghi âm", "recap nội dung audio", or "extract text from audio"
- Built-in transcription (MarkItDown, MCP audio converters) returns `Bad Request` or gibberish
- Audio file is longer than ~5 minutes and needs segmentation to avoid timeouts
- Audio is in Vietnamese or another non-English language requiring explicit language flags
- User sends `.ogg`, `.m4a`, `.mp3`, or `.wav` voice memos and expects structured output

---

## Workflow

### Step 1 — Convert to WAV (if needed)

Whisper works best with mono WAV at 16 kHz. Convert first if the source is OGG, M4A, or MP3:

```bash
ffmpeg -i input.ogg -ar 16000 -ac 1 output.wav
```

### Step 2 — Quick attempt with MarkItDown (optional)

For very short clips (< 2 min), try `mcp_markitdown_convert_to_markdown` first. If it returns `Bad Request` or nonsense, proceed to Whisper immediately.

> **Pitfall:** MarkItDown audio transcription often fails on long files, non-English audio, or noisy recordings. Do not retry more than once — switch to Whisper.

### Step 3 — Segment long files

If the file exceeds ~5 minutes, split into 2-minute chunks to keep each Whisper job fast and avoid agent timeout kills:

```bash
ffmpeg -i long_recording.wav -f segment -segment_time 120 -c copy chunk_%03d.wav
```

This produces `chunk_000.wav`, `chunk_001.wav`, etc.

> **Why segment?** Running Whisper on a 12-minute file with a `medium` model on CPU will exceed the 300–600 s agent timeout and get killed. Segmenting lets you process pieces in background batches or sequentially without losing progress.

### Step 4 — Transcribe with Whisper

Use the **small** model for the best speed/accuracy trade-off on CPU. Use **base** only if you need a rough draft fast. Avoid **medium** or **large** on CPU for long files.

Always pass the `--language` flag (e.g., `Vietnamese`) to improve accuracy.

**Single file:**
```bash
whisper input.wav --model small --language Vietnamese --output_format txt --output_dir ./
```

**Batch of segments (run in background with notify):**
```bash
whisper chunk_*.wav --model base --language Vietnamese --output_format txt --output_dir ./
```

> **Pitfall:** Whisper CLI background jobs on Windows/git-bash should set `notify_on_complete=true` so you know when segments finish.

### Step 5 — Combine and deliver

Read the generated `.txt` files (one per chunk), concatenate them in order, and present a clean, structured recap to the user. Remove duplicate "Hãy subscribe..." YouTube artifacts if the source was screen-recorded.

---

## Model Selection Guide

| Model | Speed | Accuracy | When to use |
|-------|-------|----------|-------------|
| `tiny` | Very fast | Low | Not recommended for production |
| `base` | Fast | Medium | Drafts, very long files, CPU-only |
| `small` | Moderate | Good | **Default for CPU** — best balance |
| `medium` | Slow | Very good | Only for short clips (< 3 min) on CPU |
| `large` | Very slow | Best | GPU only |

---

## References
- `references/transcription-commands.md` — Exact FFmpeg and Whisper commands used in production sessions

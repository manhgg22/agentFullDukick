---
name: media-transcription
description: Transcribe local audio and video files using openai-whisper and ffmpeg. Covers extraction, model selection, and batch processing.
triggers:
  - user asks to transcribe audio or video
  - user has media files (.mov, .mp4, .m4a, .mp3) needing text output
  - converting speech to text locally
---

# Media Transcription

## Prerequisites
- `ffmpeg` must be installed and available in the system `PATH`. Whisper's Python library calls `ffmpeg` internally via `subprocess` without an absolute path.
- **Recommended**: `faster-whisper` Python package (CTranslate2 backend, much faster on CPU).
- **Alternative**: `openai-whisper` (slower on CPU, acceptable on GPU).

## Workflow

1. **Inventory**  
   Scan the target directory recursively for media extensions: `.mov`, `.mp4`, `.m4a`, `.mp3`, `.wav`, `.avi`.

2. **Extract audio (if video)**  
   Use `ffmpeg` to convert video to 16 kHz mono WAV:
   ```bash
   ffmpeg -y -i input.mov -vn -ar 16000 -ac 1 -c:a pcm_s16le output.wav
   ```

3. **Chunk long audio (>5 min)**  
   On CPU-only machines, split into 5-minute segments to stay within sandbox timeouts (~300 s):
   ```bash
   ffmpeg -y -i long.wav -f segment -segment_time 300 -c:a copy chunk_%03d.wav
   ```
   Transcribe each chunk, then concatenate the text segments in order.

4. **Transcribe**  
   Prefer `faster-whisper` on CPU:
   ```python
   from faster_whisper import WhisperModel
   model = WhisperModel("small", device="cpu", compute_type="int8")
   segments, info = model.transcribe("output.wav", language="vi", beam_size=5)
   text = " ".join([seg.text for seg in segments])
   ```
   Fallback `openai-whisper`:
   ```python
   import whisper
   model = whisper.load_model("medium")
   result = model.transcribe("output.wav", language="vi", fp16=False)
   ```

5. **Output**  
   Save plain text or SRT depending on user preference.
   Check for existing output before transcribing to allow crash-resume.

## Model Selection

| Engine | Model | Use Case |
|--------|-------|----------|
| **faster-whisper (recommended for CPU)** | `base` | Fast draft; acceptable for clear Vietnamese |
| | `small` | Best CPU speed/accuracy trade-off for Vietnamese (~130 s per 5-min chunk on 64-core Xeon) |
| **openai-whisper (slower)** | `small` | English or high-resource languages; **avoid for Vietnamese** — accuracy is poor |
| | `medium` | Balanced speed/accuracy for Vietnamese (but ~5–8 min per 17-min video on CPU) |
| | `large` | Maximum accuracy for Vietnamese; very slow on CPU |

> **Pitfall 1 — `small` for Vietnamese**: openai-whisper `small` model produces garbled output for Vietnamese audio. When transcribing Vietnamese on CPU, prefer **faster-whisper `base` or `small`** over openai-whisper `small`/`medium`.

> **Pitfall 2 — CPU timeout on single runs**: On CPU-only machines, transcribing a 17-minute video with `medium` takes longer than most interactive sandbox timeouts (300 s). Always **chunk audio to ≤5 min segments** and process incrementally, or use `faster-whisper` with smaller model.

> **Pitfall 3 — background subprocess isolation**: On Windows, spawning a background Python process via `subprocess.Popen(..., creationflags=subprocess.CREATE_NEW_CONSOLE)` without `stdout=` redirection causes the process to hang silently when started from the sandbox. Always redirect stdout/stderr to a file. Also note that `write_file` tool fails on this Windows host when paths contain non-ASCII characters — use `execute_code` with Python `open()` instead.

## Platform Notes

- **Windows — ffmpeg PATH timing (critical)**: Whisper's Python library calls `ffmpeg` via `subprocess` at **transcribe time**, not just extraction time. Even if you pre-extracted audio with ffmpeg manually, `model.transcribe()` will still invoke ffmpeg internally and raise `FileNotFoundError` if ffmpeg is not in `os.environ["PATH"]`. 
  ```python
  import os
  ffmpeg_bin = r"D:\\...\\bin"
  if ffmpeg_bin not in os.environ.get("PATH", ""):
      os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ.get("PATH", "")
  # ONLY NOW import whisper
  import whisper
  ```

- **Windows — write_file tool limitation**: The Hermes `write_file` tool fails on this Windows host when the path contains non-ASCII/Vietnamese characters (emits "WSL has no installed distributions"). Use `execute_code` with Python `open(path, "w", encoding="utf-8")` instead.

- **CPU-only timeout pitfall**: On CPU-only machines (even 64-core Xeon), a 17-minute video with `medium` model takes ~5–8 minutes. The sandbox kills scripts exceeding 300 s. For videos >15 minutes, **pre-extract audio to WAV first** with ffmpeg, then transcribe the WAV. If still too slow, chunk the audio or switch to background execution.
  ```bash
  ffmpeg -y -i input.mov -vn -ar 16000 -ac 1 -c:a pcm_s16le output.wav
  ```

- **Large files**: Video files >1 GB will take significant time. Confirm model choice and scope with the user before batch-processing an entire directory.

## Resume / Checkpoint Pattern

When batch-processing many files, always check for existing output before transcribing:
```python
out_path = os.path.join(out_dir, basename + ".txt")
if os.path.exists(out_path):
    continue  # skip already-done files
```
This allows restarting after timeout or crash without re-doing completed work.
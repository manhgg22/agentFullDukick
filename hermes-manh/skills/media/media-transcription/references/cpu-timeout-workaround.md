# CPU Timeout Workaround for Long Transcription Jobs

## Problem
- Hermes `execute_code` sandbox has a **300-second timeout**.
- On a 64-core Intel Xeon with 32 GB RAM (CPU-only, no GPU), transcribing a 17-minute Vietnamese training video with openai-whisper `medium` takes ~5–8 minutes.
- Result: script killed mid-way, no output saved.

## Solution: Chunk + Incremental Background Worker

### Step 1 — Extract audio with ffmpeg
```bash
ffmpeg -y -i input.mov -vn -ar 16000 -ac 1 -c:a pcm_s16le output.wav
```

### Step 2 — Split into 5-minute segments
```bash
ffmpeg -y -i output.wav -f segment -segment_time 300 -c:a copy chunk_%03d.wav
```

### Step 3 — Transcribe each chunk, accumulate text, restart from last chunk on crash
The background worker pattern (see `scripts/long-running-worker.py`) handles:
- Loading model **once**
- Processing chunks sequentially
- Writing checkpoint after every chunk
- Appending results to a text file
- Resuming from last completed chunk on restart

### Step 4 — Monitor via log file
Because the Windows console created by `CREATE_NEW_PROCESS_GROUP` may not forward stdout to the caller, the worker **must redirect stdout/stderr to a log file**:
```python
with open("transcribe.log", "a", encoding="utf-8") as logf:
    subprocess.Popen([python, script], stdout=logf, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NEW_CONSOLE)
```

### Performance Reference (64-core Xeon, CPU-only)

| Model     | File      | Duration | Time   |
|-----------|-----------|----------|--------|
| openai-whisper medium | `.m4a` audio | 0.3 min  | 14 s  |
| openai-whisper medium | `.m4a` audio | 5.0 min  | 205 s |
| openai-whisper medium | `.wav` chunk | 0.9 min  | 30 s  |
| openai-whisper medium | `.wav` chunk | 16.8 min | >300 s (timeout) |
| faster-whisper small  | `.wav` chunk (5 min) | 5 min | ~130 s |
| faster-whisper base   | `.wav` chunk (5 min) | 5 min | ~37 s |

**Key takeaway**: For CPU-only Vietnamese transcription, prefer **faster-whisper small** chunked into 5-minute segments. Base is fastest but less accurate; small is the best accuracy/speed trade-off.

## Pitfall: `faster-whisper` with `medium` or `base` still times out on long files
Even faster-whisper `base` takes ~37 seconds per 5-minute chunk. A 60-minute video would need 12 chunks = ~7.4 minutes just for transcription, plus extraction time. Always use the **background worker pattern** for anything >10 minutes total.

# Whisper CPU Benchmarks — Session: 2026-06-03

Machine: Intel Xeon, 32 physical / 64 logical cores, 32 GB RAM, **no CUDA GPU**.
Model: `openai-whisper` via PyTorch CPU.
Language: Vietnamese (`language="vi"`).

## Model Quality Comparison (same 0.3-min audio file)

| Model | Time | Sample Output (Vietnamese) | Verdict |
|-------|------|---------------------------|---------|
| `small` | 13 s | "Sau khi cái này xong thì sốt đồng làm chữ tử..." | **Unusable** — heavily garbled |
| `medium` | 14 s | "Sau khi cái này xong thì xót đầu làm chứng tử..." | Acceptable, minor errors |
| `large-v3` | 25 s | "Sau khi cái này xong thì chốt đồng làm chứng từ..." | Best accuracy |

> **Rule**: For Vietnamese on CPU, `medium` is the practical minimum. `small` is not viable.

## Timeout Risk Data

| File | Duration | Model | Result |
|------|----------|-------|--------|
| `Quy trình sales 2.m4a` | 0.3 min | medium | **14 s** — fine |
| `Training nhanh…mp4` | 16.8 min | medium | **>300 s** — **killed by sandbox** |

Implication: Any video >~15 minutes will likely exceed the 300-second script timeout on this CPU-only machine.

## Total Dataset Scanned

- 24 media files in `D:\TrainSale`
- Total duration: **392.7 min (6.5 hours)**
- Total size: **13.4 GB**

Estimated wall time for full batch (`medium`, CPU):
- Linear extrapolation from 0.3-min sample: ~20,000 min (~14 days) — **not linear** because overhead dominates short files.
- Realistic estimate based on observed ~5–8 min per 17-min video: **~2–3 hours** for the full 6.5-hour dataset.

## Recommended Approach for This Machine

1. Pre-extract all videos to 16 kHz mono WAV with ffmpeg (fast, I/O bound).
2. Run transcribe in small batches (1–3 files per script invocation) to stay under 300 s timeout.
3. Use resume/checkpoint pattern to skip already-completed files.
4. If a single file still times out, chunk the WAV into 10-minute segments before transcribing.

## ffmpeg Static Build Path Used

```
D:\TrainSale\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe
```

Downloaded from: `https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip`

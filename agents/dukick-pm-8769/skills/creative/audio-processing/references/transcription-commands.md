# Transcription Command Reference

Exact commands used in a live Vietnamese audio transcription session (3 files, ~27 min total).

## 1. Convert OGG → WAV (mono 16 kHz)

```bash
ffmpeg -i input.ogg -ar 16000 -ac 1 output.wav
```

## 2. Segment long WAV into 2-minute chunks

```bash
ffmpeg -i long_recording.wav -f segment -segment_time 120 -c copy chunk_%03d.wav
```

Produces `chunk_000.wav`, `chunk_001.wav`, etc.

## 3. Transcribe with Whisper (single file)

```bash
whisper input.wav --model small --language Vietnamese --output_format txt --output_dir ./
```

## 4. Batch transcribe segments

```bash
whisper chunk_*.wav --model base --language Vietnamese --output_format txt --output_dir ./
```

## 5. Combine results

Read all generated `.txt` files in numeric order and concatenate for the final transcript.

## Lessons from this session

- MarkItDown audio converter (`mcp_markitdown_convert_to_markdown`) returned `Bad Request` on all three `.ogg` and `.wav` files. Switch to Whisper immediately — do not retry.
- `base` model on a 4.5-minute file completed in ~30 s. `medium` model on the same file exceeded 600 s timeout — killed.
- `small` model is the sweet spot for CPU-only machines.
- File 1 (4:26) transcribed cleanly. Files 2 (12:04) and 3 (10:11) required segmentation and batch background jobs.

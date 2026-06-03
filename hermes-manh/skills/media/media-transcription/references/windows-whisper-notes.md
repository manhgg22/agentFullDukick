# Windows ffmpeg + Whisper Notes

## ffmpeg availability on Windows
- `shutil.which("ffmpeg")` may return a path, but Whisper's internal `subprocess.run(["ffmpeg", ...])` still fails with `FileNotFoundError` if the directory is not in `os.environ["PATH"]`.
- **Fix**: prepend the ffmpeg `bin` directory to PATH before importing whisper:
  ```python
  import os
  os.environ["PATH"] = r"D:\TrainSale\ffmpeg\ffmpeg-master-latest-win64-gpl\bin" + os.pathsep + os.environ.get("PATH", "")
  import whisper
  ```

## Model quality for Vietnamese
- `small` model produces near-gibberish for Vietnamese audio (tested 2026-06-03 on a 2.4 MB `.m4a` training file).
- `medium` or `large` is strongly recommended.

## Batch processing checklist
1. Walk directory for `.mov`, `.mp4`, `.m4a`, `.mp3`
2. Check total size — warn user if >5 GB
3. Confirm model (`medium` vs `large`) and output format (`.txt` vs `.srt`)
4. Extract WAV with ffmpeg, transcribe, clean up WAV
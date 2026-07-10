#!/usr/bin/env python3
"""
meeting_recap.py — Transcribe + recap cuộc họp từ file audio/video.

Usage:
    python meeting_recap.py /path/to/file.mp3
    python meeting_recap.py /path/to/file.mp4

Output: recap text file cùng thư mục.
"""

import sys
import os
import subprocess
import json

def extract_audio(video_path, output_wav):
    """Extract audio từ mp4/mov/avi → wav (16kHz mono)."""
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        output_wav
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Audio extracted: {output_wav}")

def transcribe(audio_path):
    """Transcribe dùng faster-whisper (local)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Installing faster-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper", "-q"], check=True)
        from faster_whisper import WhisperModel
    
    print("Loading Whisper model (base)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    print("Transcribing...")
    segments, info = model.transcribe(audio_path, beam_size=5, language="vi")
    
    transcript = ""
    for segment in segments:
        transcript += f"[{segment.start:.2f}s → {segment.end:.2f}s] {segment.text}\n"
    
    return transcript

def generate_recap(transcript):
    """Tóm tắt transcript thành recap chuyên nghiệp."""
    # Đơn giản: nếu không có OpenAI key, trả về template
    recap = f"""# 📝 RECAP CUỘC HỌP

## 1. Tóm tắt chung
{transcript[:500]}...

## 2. Điểm chính / Quyết định
- (Cần AI model để extract chính xác)

## 3. Action Items
| Người phụ trách | Việc cần làm | Deadline |
|---|---|---|
| ? | ? | ? |

## 4. Transcript đầy đủ
```
{transcript}
```
"""
    return recap

def main():
    if len(sys.argv) < 2:
        print("Usage: python meeting_recap.py <file.mp3/mp4>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    base_dir = os.path.dirname(input_file) or "."
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Xử lý audio
    ext = os.path.splitext(input_file)[1].lower()
    if ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"]:
        audio_path = os.path.join(base_dir, f"{base_name}_audio.wav")
        extract_audio(input_file, audio_path)
    else:
        audio_path = input_file
    
    # Transcribe
    transcript = transcribe(audio_path)
    transcript_path = os.path.join(base_dir, f"{base_name}_transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"✅ Transcript saved: {transcript_path}")
    
    # Recap
    recap = generate_recap(transcript)
    recap_path = os.path.join(base_dir, f"{base_name}_recap.md")
    with open(recap_path, "w", encoding="utf-8") as f:
        f.write(recap)
    print(f"✅ Recap saved: {recap_path}")
    
    # Dọn dẹp
    if ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"] and os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"🗑️ Cleaned temp: {audio_path}")
    
    print("\n🎉 Done!")

if __name__ == "__main__":
    main()

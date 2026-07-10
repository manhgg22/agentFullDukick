#!/usr/bin/env python3
"""
meeting_recap.py - Transcribe + recap cuoc hop tu file audio/video.
Thu tu uu tien: Groq Whisper (free, nhanh) -> OpenAI Whisper API -> faster-whisper local.

Usage:
    python meeting_recap.py /path/to/file.mp3
    python meeting_recap.py /path/to/file.mp4

Output: recap text file cung thu muc (KHONG tu upload Drive - de user duyet truoc).
"""

import sys
import os
import subprocess
import json
import requests
from pathlib import Path

# ---- config ----
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
WHISPER_URL    = "https://api.openai.com/v1/audio/transcriptions"
LLM_URL        = "https://api.openai.com/v1/chat/completions"
LLM_MODEL      = "gpt-4o-mini"

# ---- helpers ----
def _load_key():
    global OPENAI_API_KEY
    if OPENAI_API_KEY:
        return
    for env_path in [
        Path(__file__).resolve().parent.parent / ".env",
        Path("/c/DuKickAgent/hermes-global.env"),
    ]:
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("OPENAI_API_KEY="):
                        OPENAI_API_KEY = line.split("=", 1)[1].strip()
                        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
                        return

_load_key()

def ensure_audio(input_path, base_dir, base_name):
    ext = os.path.splitext(input_path)[1].lower()
    audio_exts = {".mp3", ".wav", ".ogg", ".oga", ".m4a", ".flac", ".aac", ".wma"}
    if ext in audio_exts:
        return input_path
    audio_path = os.path.join(base_dir, base_name + "_audio.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vn", "-ar", "16000", "-ac", "1", "-b:a", "32k", audio_path
    ]
    print("Extracting audio from video...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Audio extracted: " + audio_path)
    return audio_path

def _transcribe_groq(audio_path):
    print("Sending to OpenAI Whisper API...")
    with open(audio_path, "rb") as f:
        resp = requests.post(
            WHISPER_URL,
            headers={"Authorization": "Bearer " + OPENAI_API_KEY},
            files={"file": (os.path.basename(audio_path), f, "audio/mpeg")},
            data={"model": "whisper-large-v3", "language": "vi", "response_format": "text"},
            timeout=300,
        )
    resp.raise_for_status()
    text = resp.text.strip()
    print(f"Transcript received ({len(text)} chars)")
    return text

def _transcribe_local(audio_path):
    print("API failed. Falling back to faster-whisper local (base)...")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Installing faster-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper", "-q"], check=True)
        from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5, language="vi")
    transcript = ""
    for segment in segments:
        transcript += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
    return transcript

def transcribe(audio_path):
    if not OPENAI_API_KEY:
        return _transcribe_local(audio_path)
    try:
        return _transcribe_groq(audio_path)
    except Exception as e:
        print(f"API error: {e}")
        return _transcribe_local(audio_path)

def generate_recap(transcript):
    prompt = (
        "Ban la tro ly ghi chep cuoc hop chuyen nghiep. "
        "Hay phan tich transcript duoi day va tom tat thanh ban recap bang tieng Viet theo cau truc:\n\n"
        "1. Tom tat chung (2-3 cau)\n"
        "2. Noi dung chinh (bullet points cac chu de da ban)\n"
        "3. Quyet dinh / Thong nhat (neu co)\n"
        "4. Action items - bang: | Nguoi phu trach (neu doan duoc) | Viec can lam | Deadline |\n\n"
        "Luu y: Neu khong ro nguoi phu trach hoac deadline thi de dau '?'. "
        "Giu giong van suc tich, de doc.\n\n"
        "TRANSCRIPT:\n---\n" + transcript + "\n---\n\n"
        "RECAP:"
    )

    if not OPENAI_API_KEY:
        return (
            "# RECAP CUOC HOP\n\n"
            "## 1. Tom tat chung\n" + transcript[:500] + "...\n\n"
            "## 2. Diem chinh / Quyet dinh\n- (Can AI model de extract chinh xac)\n\n"
            "## 3. Action Items\n| Nguoi phu trach | Viec can lam | Deadline |\n|---|---|---|\n| ? | ? | ? |\n\n"
            "## 4. Transcript day du\n```\n" + transcript + "\n```\n"
        )

    print("Generating recap with LLM...")
    resp = requests.post(
        LLM_URL,
        headers={"Authorization": "Bearer " + OPENAI_API_KEY, "Content-Type": "application/json"},
        json={"model": LLM_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3},
        timeout=120,
    )
    resp.raise_for_status()
    recap = resp.json()["choices"][0]["message"]["content"].strip()
    print(f"Recap generated ({len(recap)} chars)")
    return recap

def main():
    if len(sys.argv) < 2:
        print("Usage: python meeting_recap.py <file.mp3/mp4/ogg/wav...>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("File not found: " + input_file)
        sys.exit(1)

    base_dir  = os.path.dirname(input_file) or "."
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    audio_path = ensure_audio(input_file, base_dir, base_name)
    transcript = transcribe(audio_path)
    transcript_path = os.path.join(base_dir, base_name + "_transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print("Transcript saved: " + transcript_path)

    recap = generate_recap(transcript)
    recap_path = os.path.join(base_dir, base_name + "_recap.md")
    with open(recap_path, "w", encoding="utf-8") as f:
        f.write(recap)
    print("Recap saved: " + recap_path)

    if audio_path != input_file and os.path.exists(audio_path):
        os.remove(audio_path)
        print("Cleaned temp: " + audio_path)

    print("\nDone! Gui recap cho user duyet truoc khi luu Drive.")

if __name__ == "__main__":
    main()

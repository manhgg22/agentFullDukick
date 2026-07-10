#!/usr/bin/env python3
"""
meeting_recap.py - Transcribe + recap cuoc hop tu file audio/video.
Thu tu uu tien: Groq Whisper -> OpenAI Whisper -> faster-whisper local (small).
KHONG tu upload Drive - de user duyet truoc.

Usage:
    python meeting_recap.py /path/to/file.mp3
    python meeting_recap.py /path/to/file.mp4
"""

import sys
import os
import subprocess
import requests
from pathlib import Path

# ---- config ----
OPENAI_API_KEY=*** "")
GROQ_API_KEY=os.env...Y", "")

WHISPER_GROQ   = "https://api.groq.com/openai/v1/audio/transcriptions"
WHISPER_OPENAI = "https://api.openai.com/v1/audio/transcriptions"
LLM_GROQ       = "https://api.groq.com/openai/v1/chat/completions"
LLM_OPENAI     = "https://api.openai.com/v1/chat/completions"

LLM_MODEL_GROQ   = "llama3-8b-8192"
LLM_MODEL_OPENAI = "gpt-4o-mini"

# ---- helpers ----
def _load_keys():
    global OPENAI_API_KEY, GROQ_API_KEY
    if OPENAI_API_KEY and GROQ_API_KEY:
        return
    for env_path in [
        Path(__file__).resolve().parent.parent / ".env",
        Path("/c/DuKickAgent/hermes-global.env"),
    ]:
        if not env_path.exists():
            continue
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("OPENAI_API_KEY=***                        OPENAI_API_KEY=*** 1)[1].strip()
                if line.strip().startswith("GROQ_API_KEY=***                    GROQ_API_KEY=*** 1)[1].strip()

_load_keys()

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
    print("Sending to Groq Whisper API (whisper-large-v3)...")
    with open(audio_path, "rb") as f:
        resp = requests.post(
            WHISPER_GROQ,
            headers={"Authorization": "Bearer " + GROQ_API_KEY},
            files={"file": (os.path.basename(audio_path), f, "audio/mpeg")},
            data={"model": "whisper-large-v3", "language": "vi", "response_format": "text"},
            timeout=300,
        )
    resp.raise_for_status()
    text = resp.text.strip()
    print(f"Transcript received ({len(text)} chars)")
    return text

def _transcribe_openai(audio_path):
    print("Sending to OpenAI Whisper API...")
    with open(audio_path, "rb") as f:
        resp = requests.post(
            WHISPER_OPENAI,
            headers={"Authorization": "Bearer " + OPENAI_API_KEY},
            files={"file": (os.path.basename(audio_path), f, "audio/mpeg")},
            data={"model": "whisper-1", "language": "vi", "response_format": "text"},
            timeout=300,
        )
    resp.raise_for_status()
    text = resp.text.strip()
    print(f"Transcript received ({len(text)} chars)")
    return text

def _transcribe_local(audio_path):
    print("API failed. Falling back to faster-whisper local (small model)...")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Installing faster-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper", "-q"], check=True)
        from faster_whisper import WhisperModel
    # ⚠️ Dùng "small" cho tiếng Việt — "base" ra gibberish
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5, language="vi")
    transcript = " ".join([seg.text for seg in segments])
    print(f"Local transcript done ({len(transcript)} chars)")
    return transcript

def transcribe(audio_path):
    # Thu tu uu tien: Groq -> OpenAI -> local
    if GROQ_API_KEY:
        try:
            return _transcribe_groq(audio_path)
        except Exception as e:
            print(f"Groq error: {e}")
    if OPENAI_API_KEY:
        try:
            return _transcribe_openai(audio_path)
        except Exception as e:
            print(f"OpenAI error: {e}")
    return _transcribe_local(audio_path)

def _recap_llm(transcript, url, key, model):
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
    print("Generating recap with LLM...")
    resp = requests.post(
        url,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3},
        timeout=120,
    )
    resp.raise_for_status()
    recap = resp.json()["choices"][0]["message"]["content"].strip()
    print(f"Recap generated ({len(recap)} chars)")
    return recap

def _recap_manual(transcript):
    # Fallback khi khong co API
    return (
        "# RECAP CUOC HOP\n\n"
        "## 1. Tom tat chung\n" + transcript[:500] + "...\n\n"
        "## 2. Diem chinh / Quyet dinh\n- (Can AI model de extract chinh xac)\n\n"
        "## 3. Action Items\n| Nguoi phu trach | Viec can lam | Deadline |\n|---|---|---|\n| ? | ? | ? |\n\n"
        "## 4. Transcript day du\n```\n" + transcript + "\n```\n"
    )

def generate_recap(transcript):
    if GROQ_API_KEY:
        try:
            return _recap_llm(transcript, LLM_GROQ, GROQ_API_KEY, LLM_MODEL_GROQ)
        except Exception as e:
            print(f"Groq LLM error: {e}")
    if OPENAI_API_KEY:
        try:
            return _recap_llm(transcript, LLM_OPENAI, OPENAI_API_KEY, LLM_MODEL_OPENAI)
        except Exception as e:
            print(f"OpenAI LLM error: {e}")
    return _recap_manual(transcript)

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

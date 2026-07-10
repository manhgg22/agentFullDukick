@echo off
cd /d C:\DuKickAgent\agents\dukick-thuno-8773
set PYTHONIOENCODING=utf-8
set OPENAI_API_KEY=***REMOVED***
set OPENAI_BASE_URL=https://ollama.com/v1
set AI_MODEL=glm-5.2
C:/DukickAgent/venv/Scripts/python.exe scripts/webhook_server.py
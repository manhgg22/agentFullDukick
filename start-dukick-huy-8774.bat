@echo off
cd /d C:\DuKickAgent\agents\dukick-huy-8774
call C:\DukickAgent\venv\Scripts\activate.bat
set HERMES_HOME=C:\DuKickAgent\agents\dukick-huy-8774
set PYTHONIOENCODING=utf-8
C:\DukickAgent\venv\Scripts\python.exe -m hermes_cli.main gateway run --replace --accept-hooks
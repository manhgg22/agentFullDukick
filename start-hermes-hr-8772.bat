@echo off
cd /d C:\DuKickAgent\agents\hermes-hr-8772
call C:\DuKickAgent\venv\Scripts\activate.bat
set HERMES_HOME=C:\DuKickAgent\agents\hermes-hr-8772
C:\DuKickAgent\venv\Scripts\python.exe -m hermes_cli.main gateway run --replace --accept-hooks

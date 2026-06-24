@echo off
set HERMES_HOME=C:/DuKickAgent/agents/dukick-pmcreative-8770
set PYTHONIOENCODING=utf-8
C:/DukickAgent/venv/Scripts/python.exe -m hermes_cli.main gateway run --replace --accept-hooks

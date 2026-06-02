@echo off 
set HERMES_HOME=C:/DuKickAgent/dukick-pm-8769 
set PYTHONIOENCODING=utf-8 
C:/DuKickAgent/venv/Scripts/python.exe -m hermes_cli.main gateway run --replace 

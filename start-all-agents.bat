@echo off
cd /d C:\DuKickAgent
timeout /t 10 /nobreak >nul

start "" /min "C:\DuKickAgent\start-dukick-truyenthong-8768.bat"
timeout /t 3 /nobreak >nul
start "" /min "C:\DuKickAgent\start-dukick-pm-8769.bat"
timeout /t 3 /nobreak >nul
start "" /min "C:\DuKickAgent\start-dukick-pmcreative-8770.bat"
timeout /t 3 /nobreak >nul
start "" /min "C:\DuKickAgent\start-dukick-ketoan-8771.bat"
timeout /t 3 /nobreak >nul
start "" /min "C:\DuKickAgent\start-hermes-hr-8772.bat"
timeout /t 8 /nobreak >nul
start "" /min "C:\DuKickAgent\start-dukick-tong-8767.bat"

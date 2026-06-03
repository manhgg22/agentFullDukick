# DuKick - Auto backfill Discord messages to Obsidian (runs every hour)
$logFile = "C:\DuKickAgent\logs\backfill.log"
New-Item -ItemType Directory -Path "C:\DuKickAgent\logs" -Force | Out-Null
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$ts Running backfill..." | Out-File $logFile -Append -Encoding utf8
$env:PYTHONIOENCODING = "utf-8"
$result = & "C:/DuKickAgent/venv/Scripts/python.exe" "C:/DuKickAgent/backfill_obsidian.py" 2>&1
$result | Out-File $logFile -Append -Encoding utf8
"$ts Done." | Out-File $logFile -Append -Encoding utf8

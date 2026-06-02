$env:HERMES_HOME = "C:/DuKickAgent/dukick-pm-8769"
$env:PYTHONIOENCODING = "utf-8"
& "C:/DuKickAgent/venv/Scripts/python.exe" -m hermes_cli.main gateway run --replace --accept-hooks

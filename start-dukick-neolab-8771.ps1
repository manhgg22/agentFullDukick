$env:HERMES_HOME = "C:/DuKickAgent/dukick-neolab-8771"
$env:PYTHONIOENCODING = "utf-8"
& "C:/DuKickAgent/venv/Scripts/python.exe" -m hermes_cli.main gateway run --replace --accept-hooks

# DuKick — Hourly pipeline: Discord → Obsidian → Quartz → Web
$logFile = "C:\DuKickAgent\logs\backfill.log"
New-Item -ItemType Directory -Path "C:\DuKickAgent\logs" -Force | Out-Null
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$ts [START] Backfill pipeline" | Out-File $logFile -Append -Encoding utf8

# Step 1: Backfill Discord → Obsidian
"$ts [1/3] Fetching Discord messages..." | Out-File $logFile -Append -Encoding utf8
$env:PYTHONIOENCODING = "utf-8"
$r1 = & "C:/DuKickAgent/venv/Scripts/python.exe" "C:/DuKickAgent/backfill_obsidian.py" 2>&1
$r1 | Out-File $logFile -Append -Encoding utf8

# Step 2: Rebuild Quartz
"$ts [2/3] Rebuilding Quartz website..." | Out-File $logFile -Append -Encoding utf8

# Sync vault content vào Quartz
$vaultRoot = "C:\Users\Admin\Documents\Obsidian Vault"
$quartzContent = "C:\DuKickAgent\dukick-obsidian-web\content"
$vaults = @("DuKick-Tong","DuKick-TruyenThong","DuKick-PM","DuKick-PMCreative","DuKick-NeoLab","Hanoi-Signature","Photoshoot-HNS")
foreach ($v in $vaults) {
    $dest = "$quartzContent\$v"
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Get-ChildItem "$vaultRoot\$v" -Recurse -Filter "*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        $rel = $_.FullName.Substring("$vaultRoot\$v".Length)
        $target = "$dest$rel"
        New-Item -ItemType Directory -Path (Split-Path $target) -Force | Out-Null
        Copy-Item $_.FullName $target -Force
    }
}

$proc = Start-Process "node" -ArgumentList "quartz/bootstrap-cli.mjs build" `
    -WorkingDirectory "C:\DuKickAgent\dukick-obsidian-web" `
    -NoNewWindow -PassThru `
    -RedirectStandardOutput "C:\DuKickAgent\logs\quartz-build.log" `
    -RedirectStandardError "C:\DuKickAgent\logs\quartz-err.log"
$proc.WaitForExit(120000)
"$ts [2/3] Quartz build done: exit=$($proc.ExitCode)" | Out-File $logFile -Append -Encoding utf8

# Step 3: Restart web server
"$ts [3/3] Restarting web server..." | Out-File $logFile -Append -Encoding utf8
pm2 restart dukick-obsidian 2>&1 | Out-File $logFile -Append -Encoding utf8

$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$ts [DONE] Pipeline complete" | Out-File $logFile -Append -Encoding utf8

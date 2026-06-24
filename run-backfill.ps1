# Dukick — Hourly pipeline: Discord → Obsidian → Quartz → Web
$logFile = "C:\DukickAgent\logs\backfill.log"
New-Item -ItemType Directory -Path "C:\DukickAgent\logs" -Force | Out-Null
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$ts [START] Backfill pipeline" | Out-File $logFile -Append -Encoding utf8

# Step 1: Backfill Discord → Obsidian
"$ts [1/3] Fetching Discord messages..." | Out-File $logFile -Append -Encoding utf8
$env:PYTHONIOENCODING = "utf-8"
$r1 = & "C:/DukickAgent/venv/Scripts/python.exe" "C:/DukickAgent/backfill_obsidian.py" 2>&1
$r1 | Out-File $logFile -Append -Encoding utf8

# Step 2: Rebuild Quartz
"$ts [2/3] Rebuilding Quartz website..." | Out-File $logFile -Append -Encoding utf8

# Sync vault content vào Quartz
$vaultRoot = "C:\Users\Admin\Documents\Obsidian Vault"
$quartzContent = "C:\DukickAgent\Dukick-obsidian-web\content"
$vaults = @("Dukick-Tong","Dukick-TruyenThong","Dukick-PM","Dukick-PMCreative","Dukick-NeoLab","Hanoi-Signature","Photoshoot-HNS")
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
    -WorkingDirectory "C:\DukickAgent\Dukick-obsidian-web" `
    -NoNewWindow -PassThru `
    -RedirectStandardOutput "C:\DukickAgent\logs\quartz-build.log" `
    -RedirectStandardError "C:\DukickAgent\logs\quartz-err.log"
$proc.WaitForExit(120000)
"$ts [2/3] Quartz build done: exit=$($proc.ExitCode)" | Out-File $logFile -Append -Encoding utf8

# Step 3: Restart web server
"$ts [3/3] Restarting web server..." | Out-File $logFile -Append -Encoding utf8
pm2 restart Dukick-obsidian 2>&1 | Out-File $logFile -Append -Encoding utf8

$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$ts [DONE] Pipeline complete" | Out-File $logFile -Append -Encoding utf8

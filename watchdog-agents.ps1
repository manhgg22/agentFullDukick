
$agents = @(
    @{name="dukick-tong-8767"; bat="start-dukick-tong-8767.bat"; last=1},
    @{name="dukick-truyenthong-8768"; bat="start-dukick-truyenthong-8768.bat"; last=0},
    @{name="dukick-pm-8769"; bat="start-dukick-pm-8769.bat"; last=0},
    @{name="dukick-pmcreative-8770"; bat="start-dukick-pmcreative-8770.bat"; last=0},
    @{name="dukick-ketoan-8771"; bat="start-dukick-ketoan-8771.bat"; last=0},
    @{name="hermes-hr-8772"; bat="start-hermes-hr-8772.bat"; last=0}
)

$dead = @()
foreach ($a in $agents) {
    $pidFile = "C:\DuKickAgent\agents\$($a.name)\gateway.pid"
    $p = if (Test-Path $pidFile) { (Get-Content $pidFile | ConvertFrom-Json).pid } else { $null }
    $alive = if ($p) { $null -ne (Get-Process -Id $p -ErrorAction SilentlyContinue) } else { $false }
    if (-not $alive) { $dead += $a }
}

if ($dead.Count -eq 0) { exit 0 }

# Start non-tong first
foreach ($a in ($dead | Where-Object { $_.last -eq 0 })) {
    Start-Process -FilePath "C:\DuKickAgent\$($a.bat)" -WorkingDirectory "C:\DuKickAgent" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# Tong last
if ($dead | Where-Object { $_.last -eq 1 }) {
    Start-Sleep -Seconds 8
    Start-Process -FilePath "C:\DuKickAgent\start-dukick-tong-8767.bat" -WorkingDirectory "C:\DuKickAgent" -WindowStyle Hidden
}

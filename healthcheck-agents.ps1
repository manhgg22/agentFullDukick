# DuKick - Health Check & Auto-restart stale agents
$logFile = "C:\DuKickAgent\logs\healthcheck.log"
New-Item -ItemType Directory -Path "C:\DuKickAgent\logs" -Force | Out-Null

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts $msg" | Out-File $logFile -Append -Encoding utf8
}

$agents = @(
    "dukick-truyenthong-8768",
    "dukick-pm-8769",
    "dukick-pmcreative-8770",
    "dukick-ketoan-8771",
    "dukick-tong-8767"
)

foreach ($a in $agents) {
    $stateFile = "C:\DuKickAgent\$a\gateway_state.json"
    if (-not (Test-Path $stateFile)) { continue }

    $state = Get-Content $stateFile | ConvertFrom-Json
    $discordState = $state.platforms.discord.state
    $updatedAt = [datetime]$state.updated_at
    $minutesOld = ((Get-Date).ToUniversalTime() - $updatedAt).TotalMinutes
    $gPid = $state.pid

    # Stale nếu: discord không phải "connected" HOẶC không update > 30 phút
    $isStale = ($discordState -ne "connected") -or ($minutesOld -gt 30)

    if ($isStale) {
        Log "STALE: $a (state=$discordState, age=${minutesOld}min) — restarting..."

        # Kill process cũ
        Stop-Process -Id $gPid -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2

        # Xóa lock files
        Remove-Item "C:\DuKickAgent\$a\gateway.lock" -Force -ErrorAction SilentlyContinue
        Remove-Item "C:\DuKickAgent\$a\gateway.pid" -Force -ErrorAction SilentlyContinue

        # Restart
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "C:/DuKickAgent/venv/Scripts/python.exe"
        $psi.Arguments = "-m hermes_cli.main gateway run --accept-hooks"
        $psi.UseShellExecute = $false
        $psi.CreateNoWindow = $true
        $psi.Environment["HERMES_HOME"] = "C:/DuKickAgent/$a"
        $psi.Environment["PYTHONIOENCODING"] = "utf-8"
        $psi.Environment["PATH"] = $env:PATH
        [System.Diagnostics.Process]::Start($psi) | Out-Null
        Start-Sleep -Seconds 5

        Log "RESTARTED: $a"
    }
}

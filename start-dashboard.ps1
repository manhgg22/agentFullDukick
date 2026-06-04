# DuKick Dashboard — Start 5 Hermes Web UI instances
# Moi agent chay tren 1 port rieng voi home rieng

$env:PATH = "C:\DuKickAgent\venv\Scripts;" + $env:PATH
$env:PYTHONIOENCODING = "utf-8"

$agents = @(
    @{name="dukick-tong-8767";        port=9001; label="Tong Coordinator"},
    @{name="dukick-truyenthong-8768"; port=9002; label="Sales"},
    @{name="dukick-pm-8769";          port=9003; label="Account"},
    @{name="dukick-pmcreative-8770";  port=9004; label="Creative"},
    @{name="dukick-ketoan-8771";      port=9005; label="Finance"}
)

# Stop existing instances
foreach ($a in $agents) {
    $stateDir = "C:\Users\Admin\.hermes-webui-$($a.name)"
    $pidFile = "$stateDir\server.pid"
    if (Test-Path $pidFile) {
        $oldPid = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($oldPid) { Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue }
    }
}
Start-Sleep -Seconds 2

# Start each instance
foreach ($a in $agents) {
    $stateDir = "C:\Users\Admin\.hermes-webui-$($a.name)"
    New-Item -ItemType Directory -Path $stateDir -Force | Out-Null

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "node"
    $psi.Arguments = "C:\DuKickAgent\hermes-webui\bin\hermes-web-ui.mjs start --port $($a.port)"
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.Environment["HERMES_HOME"] = "C:/DuKickAgent/$($a.name)"
    $psi.Environment["HERMES_WEB_UI_HOME"] = $stateDir
    $psi.Environment["PATH"] = $env:PATH
    $psi.Environment["PYTHONIOENCODING"] = "utf-8"
    [System.Diagnostics.Process]::Start($psi) | Out-Null

    Start-Sleep -Seconds 3
    Write-Host "Started $($a.label) on port $($a.port)"
}

Write-Host ""
Write-Host "DuKick Dashboard Hub:"
Write-Host "  http://localhost:9001  (Tong)"
Write-Host "  http://localhost:9002  (Sales)"
Write-Host "  http://localhost:9003  (Account)"
Write-Host "  http://localhost:9004  (Creative)"
Write-Host "  http://localhost:9005  (Finance)"
Write-Host "  Hub page: http://localhost:9001/dukick.html"

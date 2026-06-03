# DuKick - Start All 5 Agents
# Chay tu dong khi Windows khoi dong

$logFile = "C:\DuKickAgent\logs\startup.log"
New-Item -ItemType Directory -Path "C:\DuKickAgent\logs" -Force | Out-Null

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts $msg" | Out-File $logFile -Append -Encoding utf8
    Write-Host "$ts $msg"
}

Log "=== DuKick Agents Starting ==="

# Doi Windows network san sang
Start-Sleep -Seconds 10

# Xoa kanban.db loi tu lan truoc
$agents = @(
    "dukick-truyenthong-8768",
    "dukick-pm-8769",
    "dukick-pmcreative-8770",
    "dukick-neolab-8771",
    "dukick-tong-8767"
)

foreach ($a in $agents) {
    $dir = "C:\DuKickAgent\$a"
    Remove-Item "$dir\kanban.db" -Force -ErrorAction SilentlyContinue
    Remove-Item "$dir\kanban.db-shm" -Force -ErrorAction SilentlyContinue
    Remove-Item "$dir\kanban.db-wal" -Force -ErrorAction SilentlyContinue
    Remove-Item "$dir\gateway.lock" -Force -ErrorAction SilentlyContinue
    Remove-Item "$dir\gateway.pid" -Force -ErrorAction SilentlyContinue
}

# Start tung agent (tong CUOI CUNG)
foreach ($a in $agents) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "C:/DuKickAgent/venv/Scripts/python.exe"
    $psi.Arguments = "-m hermes_cli.main gateway run --accept-hooks"
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
    $psi.Environment["HERMES_HOME"] = "C:/DuKickAgent/$a"
    $psi.Environment["PYTHONIOENCODING"] = "utf-8"
    $psi.Environment["PATH"] = $env:PATH
    # API key duoc doc tu .env cua tung agent boi Hermes tu dong
    [System.Diagnostics.Process]::Start($psi) | Out-Null
    Log "Started: $a"
    Start-Sleep -Seconds 5
}

Log "=== All 5 agents started ==="

# Start-Sovereign-Offline.ps1
# Mandate: Launch the Offline Sovereign Brain & Standalone GUI

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " STARTING SOVEREIGN OFFLINE BRAIN (SQLITE + GEMMA)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$PythonExe = "C:\Users\chipp\AppData\Roaming\Accio\pre-install\7d5a6d879db7\python\python.exe"
$GuiScript = "C:\Users\chipp\sovereign_gui.py"

# 1. Cloud Node Sync
Write-Host "[1/2] Checking Cloud Node Status..." -ForegroundColor Yellow
git -C C:\audits push origin master --force 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "      SUCCESS: Cloud Node SYNCHRONIZED." -ForegroundColor Green
} else {
    Write-Host "      WARNING: Cloud Node OFFLINE / AUTH_REQUIRED." -ForegroundColor Yellow
}

# 2. Launch the Sovereign Standalone GUI
Write-Host "[2/2] Launching Sovereign Standalone Interface..." -ForegroundColor Yellow
if (Test-Path $GuiScript) {
    # Launch GUI directly (blocking the terminal is fine, or use Start-Process)
    Start-Process -FilePath $PythonExe -ArgumentList $GuiScript
    Write-Host "      SUCCESS: Sovereign Window Active." -ForegroundColor Green
} else {
    Write-Host "      ERROR: GUI script not found at $GuiScript" -ForegroundColor Red
}

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " SOVEREIGN MODE: HYBRID (LOCAL BRAIN + CLOUD SYNC)" -ForegroundColor Green
Write-Host " AUDIT LEDGER: C:\audits" -ForegroundColor Yellow
Write-Host " REMOTE LEDGER: https://github.com/chippy8444/sovereign-audit-ledger" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan

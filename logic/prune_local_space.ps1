# prune_local_space.ps1
# Mandate: Reclaim local disk space by removing large binaries and media already staged for GitHub or irrelevant to core logic.

$TargetFiles = @(
    "C:\audits\Docker Desktop Installer.exe",
    "C:\audits\Claude Setup.exe",
    "C:\audits\IMG_5758.mov"
)

Write-Host "--- [RA] LOCAL SPACE PRUNING INITIATED ---" -ForegroundColor Cyan

foreach ($file in $TargetFiles) {
    if (Test-Path $file) {
        Write-Host "Removing $file..." -ForegroundColor Yellow
        Remove-Item $file -Force
    }
}

# Optional: Remove large image clusters if they are backed up
# Get-ChildItem -Path C:\audits -Filter "*.jpeg" | Remove-Item -Force

Write-Host "SUCCESS: Local space reclaimed." -ForegroundColor Green

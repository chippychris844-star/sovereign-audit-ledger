# backfill_to_github.ps1
# Mandate: Comprehensive backfill of the Sovereign Audit Ledger and Core Logic.

$RepoPath = "C:\audits"
cd $RepoPath

Write-Host "--- [RA] SOVEREIGN BACKFILL INITIATED ---" -ForegroundColor Cyan

# 1. Update Ignore Rules for Maximum Logic Retention
$IgnoreContent = @'
node_modules/
*.RIP/
*.ldb
*.log.*
# Allow specific forensic artifacts
!USER_ONLY_CHAT_EXTRACT.json
!ONEDRIVE_DIAGNOSTICS_EXTRACT.txt
!CHATGPT_EDGE_EXTRACT.json
!CLAUDE_EDGE_EXTRACT.json
!sre_core/sovereign_brain.sqlite
'@
Set-Content -Path ".gitignore" -Value $IgnoreContent

# 2. Stage Core Components
Write-Host "Staging Core Components..." -ForegroundColor Yellow
git add .

# 3. Commit
Write-Host "Creating Truth-Ledger Commit..." -ForegroundColor Yellow
git commit -m "Sovereign Backfill: Consolidated Forensic Ledger and SRE Core Logic"

# 4. Final Push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
# Note: This will fail if the remote repo doesn't exist.
git push origin master --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Sovereign Backfill Complete." -ForegroundColor Green
} else {
    Write-Host "ERROR: GitHub Push Failed. Ensure repository 'sovereign-audit-ledger' is created on GitHub." -ForegroundColor Red
}

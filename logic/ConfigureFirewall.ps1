# ConfigureFirewall.ps1
# Run as Administrator
# Creates Windows Firewall rules to block known malicious destinations

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FIREWALL CONFIGURATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$blockedDomains = @(
    'alibaba.com',
    'alicdn.com',
    'mmstat.com',
    'phoenix-gw.alibaba.com',
    'iflow.alibaba.com',
    'acs.aliyun.com',
    'alidns.com',
    'aliyun.com'
)

$blockedIPs = @(
    # Alibaba infrastructure - add specific IPs if known from Fiddler logs
)

Write-Host "Creating outbound firewall rules..." -ForegroundColor Cyan
Write-Host ""

foreach ($domain in $blockedDomains) {
    $ruleName = "Block-$domain"

    # Check if rule already exists
    $existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

    if ($existingRule) {
        Write-Host "  ⓘ Rule already exists: $ruleName" -ForegroundColor Yellow
    }
    else {
        try {
            New-NetFirewallRule -DisplayName $ruleName `
                -Direction Outbound `
                -Action Block `
                -RemoteAddress $domain `
                -Protocol TCP `
                -ErrorAction Stop

            Write-Host "  ✓ Created: $ruleName" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ Failed to create: $ruleName - $_" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FIREWALL RULES CONFIGURED" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To view rules:" -ForegroundColor Cyan
Write-Host "  Settings → Privacy & Security → Windows Firewall → Advanced Settings"
Write-Host ""
Write-Host "To view blocked connection attempts:" -ForegroundColor Cyan
Write-Host "  Event Viewer → Windows Logs → Security → Audit Failure"
Write-Host ""

# List all custom firewall rules
Write-Host "Current custom rules:" -ForegroundColor Cyan
Get-NetFirewallRule | Where-Object { $_.DisplayName -like "Block-*" } | Select-Object DisplayName, Direction, Action | Format-Table -AutoSize

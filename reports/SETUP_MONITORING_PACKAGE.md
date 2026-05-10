# Cross-Device Monitoring & Defensive Setup Package
**Date Created:** 2026-05-05  
**Purpose:** Deploy network monitoring, task auditing, and tracking prevention on secondary laptop

---

## Part 1: Pre-Setup Checklist

- [ ] Secondary laptop has Administrator access
- [ ] Internet connection available (for tool downloads)
- [ ] USB drive or network share for file transfer
- [ ] 2GB free disk space minimum
- [ ] Windows 10/11 (x64)

---

## Part 2: Fiddler Classic Installation & Configuration

### Step 1: Download & Install
1. Visit: https://www.telerik.com/fiddler/fiddler-classic
2. Click "Download Fiddler Classic" (free version)
3. Install to: `C:\Program Files\Fiddler Classic\`
4. Run as Administrator on first launch

### Step 2: Enable HTTPS Decryption
1. Open Fiddler → Tools → Options → HTTPS
2. Check: "Capture HTTPS CONNECTs"
3. Check: "Decrypt HTTPS traffic"
4. Click "Actions" → "Trust Root Certificate"
5. Click "Yes" to install certificate

### Step 3: Configure Logging
1. File → Capture Traffic (toggle ON)
2. Tools → Options → Logging
3. Set log path: `C:\Logs\Fiddler\` (create folder if needed)
4. Enable "Log all sessions to file"
5. Set filename template: `fiddler_YYYYMMDD_HHMMSS.saz`

### Step 4: Blacklist Suspicious Destinations
1. Tools → Options → Filters
2. Add filter rule: Hostname contains `alibaba.com` → Action: Block
3. Add filter rule: Hostname contains `alicdn.com` → Action: Block
4. Add filter rule: Hostname contains `mmstat.com` → Action: Block
5. Add filter rule: Hostname contains `phoenix-gw` → Action: Block

---

## Part 3: Task Scheduler Audit Scripts

### Script 1: Export All Scheduled Tasks

**File:** `ExportScheduledTasks.ps1`

```powershell
# Run as Administrator
# Creates timestamped export of all scheduled tasks

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outputDir = "C:\Logs\TaskScheduler"
$csvOutput = "$outputDir\AllScheduledTasks_$timestamp.csv"
$xmlDir = "$outputDir\TaskExports_$timestamp"

# Create directories
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force }
if (-not (Test-Path $xmlDir)) { New-Item -ItemType Directory -Path $xmlDir -Force }

# Export all tasks to CSV
Write-Host "Exporting all scheduled tasks to CSV..."
Get-ScheduledTask | Select-Object TaskName, TaskPath, State, Date, Author, Actions, Triggers | Export-Csv -Path $csvOutput -NoTypeInformation

# Export suspicious task names to detailed XML
Write-Host "Exporting detailed task definitions..."
$suspiciousTasks = Get-ScheduledTask | Where-Object { 
    $_.TaskName -match 'Resolution|Register|RA-|Accio|Coder|Base44|Cognitive|Trap|Injector|Ingest|Nexus|Weaver|Leviathan|Genesis|Phoenix' 
}

foreach ($task in $suspiciousTasks) {
    $taskName = $task.TaskName -replace '[\\/:*?"<>|]', '_'
    $xmlFile = "$xmlDir\$taskName.xml"
    Export-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath | Out-File -FilePath $xmlFile
    Write-Host "  Exported: $($task.TaskName)"
}

Write-Host ""
Write-Host "✓ Export complete"
Write-Host "  CSV: $csvOutput"
Write-Host "  XML Details: $xmlDir"
```

**Run:**
```powershell
powershell -ExecutionPolicy Bypass -File "C:\setup\ExportScheduledTasks.ps1"
```

---

### Script 2: Monitor Task Execution in Real-Time

**File:** `MonitorTaskExecution.ps1`

```powershell
# Run as Administrator
# Monitors and logs all task execution attempts

$logFile = "C:\Logs\TaskScheduler\TaskExecution_$(Get-Date -Format 'yyyyMMdd').log"
$logDir = Split-Path $logFile
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force }

Write-Host "Starting real-time task monitor..."
Write-Host "Log file: $logFile"
Write-Host "Press Ctrl+C to stop`n"

# Get initial state
$previousTasks = @()

while ($true) {
    $currentTasks = Get-ScheduledTask | Where-Object { $_.State -eq 'Running' }
    
    # Find newly launched tasks
    $newTasks = $currentTasks | Where-Object { $_.TaskName -notin $previousTasks.TaskName }
    
    foreach ($task in $newTasks) {
        $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - TASK LAUNCHED: $($task.TaskName) | Path: $($task.TaskPath)"
        Write-Host $logEntry -ForegroundColor Yellow
        Add-Content -Path $logFile -Value $logEntry
    }
    
    $previousTasks = $currentTasks
    Start-Sleep -Seconds 5
}
```

**Run in persistent window:**
```powershell
powershell -ExecutionPolicy Bypass -File "C:\setup\MonitorTaskExecution.ps1"
```

---

### Script 3: Disable Suspicious Tasks

**File:** `DisableSuspiciousTasks.ps1`

```powershell
# Run as Administrator
# CAUTION: Only run after reviewing exported tasks

$suspiciousPatterns = @(
    'Resolution*',
    'Register*',
    '*Cognitive*',
    '*Trap*',
    '*Injector*',
    '*Accio*',
    '*Coder*',
    '*Base44*'
)

Write-Host "WARNING: This will disable tasks matching suspicious patterns"
Write-Host "Review C:\Logs\TaskScheduler\AllScheduledTasks_*.csv first"
Write-Host ""
Read-Host "Press Enter to continue or Ctrl+C to cancel"

foreach ($pattern in $suspiciousPatterns) {
    $tasks = Get-ScheduledTask | Where-Object { $_.TaskName -like $pattern }
    
    foreach ($task in $tasks) {
        Write-Host "Disabling: $($task.TaskName)"
        Disable-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath -Confirm:$false
    }
}

Write-Host "`n✓ Suspicious tasks disabled"
```

---

## Part 4: Firewall Configuration

### Windows Defender Firewall Rules

**File:** `ConfigureFirewall.ps1`

```powershell
# Run as Administrator
# Blocks known malicious destinations

$blockedDomains = @(
    'alibaba.com',
    'alicdn.com',
    'mmstat.com',
    'phoenix-gw.alibaba.com',
    'iflow.alibaba.com',
    'acs.aliyun.com'
)

Write-Host "Configuring Windows Firewall..."

foreach ($domain in $blockedDomains) {
    # Add outbound firewall rule
    $ruleName = "Block-$domain"
    Write-Host "Creating rule: $ruleName"
    
    New-NetFirewallRule -DisplayName $ruleName `
        -Direction Outbound `
        -Action Block `
        -RemoteAddress $domain `
        -Protocol TCP `
        -ErrorAction SilentlyContinue
}

Write-Host "`n✓ Firewall rules configured"
Write-Host "View rules in: Settings → Privacy & Security → Windows Firewall → Advanced Settings"
```

---

## Part 5: Network Traffic Logging

### Enable Windows Network Tracing

**File:** `EnableNetworkTracing.ps1`

```powershell
# Run as Administrator
# Captures all network connections for forensic analysis

$logDir = "C:\Logs\Network"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force }

Write-Host "Enabling network diagnostics..."

# Enable network trace
New-NetEventSession -Name "CaptureSuspiciousTraffic" -CaptureMode SaveToFile -LocalFilePath "$logDir\network_trace.etl" -ErrorAction SilentlyContinue

# Add IPv4 provider
Add-NetEventPacketCaptureProvider -SessionName "CaptureSuspiciousTraffic" -Level 3 -ErrorAction SilentlyContinue

# Start capture
Start-NetEventSession -Name "CaptureSuspiciousTraffic" -ErrorAction SilentlyContinue

Write-Host "`n✓ Network tracing started"
Write-Host "Location: $logDir\network_trace.etl"
Write-Host "To stop: Stop-NetEventSession -Name 'CaptureSuspiciousTraffic'"
```

---

## Part 6: Evidence Preservation Checklist

Create folder: `C:\Evidence\`

**Daily Export Routine:**

```batch
@echo off
REM Run this batch file daily as Administrator

set TIMESTAMP=%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set EVIDENCE_DIR=C:\Evidence\%TIMESTAMP%

mkdir %EVIDENCE_DIR%

REM Export Task Scheduler
powershell -Command "Get-ScheduledTask | Export-Csv -Path '%EVIDENCE_DIR%\ScheduledTasks.csv' -NoTypeInformation"

REM Export Event Logs
wevtutil epl System "%EVIDENCE_DIR%\System.evtx"
wevtutil epl Security "%EVIDENCE_DIR%\Security.evtx"
wevtutil epl Application "%EVIDENCE_DIR%\Application.evtx"

REM Export Network Connections
netstat -ano > "%EVIDENCE_DIR%\netstat.txt"

REM Export Processes
tasklist /v > "%EVIDENCE_DIR%\processes.txt"

REM Export Fiddler logs
if exist "C:\Logs\Fiddler\" (
    xcopy "C:\Logs\Fiddler\*.saz" "%EVIDENCE_DIR%\Fiddler\" /Y
)

echo Evidence exported to: %EVIDENCE_DIR%
pause
```

Save as: `C:\setup\DailyEvidenceExport.bat`

Schedule in Task Scheduler:
- Trigger: Daily at 21:00
- Action: Run `C:\setup\DailyEvidenceExport.bat`

---

## Part 7: Installation Order

**On Secondary Laptop:**

1. Create folder structure:
   ```
   C:\setup\
   C:\Logs\Fiddler\
   C:\Logs\TaskScheduler\
   C:\Logs\Network\
   C:\Evidence\
   ```

2. Copy all `.ps1` files to `C:\setup\`

3. Copy `DailyEvidenceExport.bat` to `C:\setup\`

4. Install Fiddler Classic (Part 2)

5. Run: `ExportScheduledTasks.ps1` (creates baseline)

6. Run: `ConfigureFirewall.ps1` (blocks destinations)

7. Run: `EnableNetworkTracing.ps1` (starts capture)

8. Schedule: `DailyEvidenceExport.bat` in Task Scheduler

9. Start: `MonitorTaskExecution.ps1` in persistent PowerShell window

---

## Part 8: Transfer to Law Enforcement

**Evidence packages ready for:**
- AFP Cyber Crime
- State Police
- ACCC
- Privacy Commissioner

**File structure for handover:**
```
Evidence_Package_20260505\
├── ScheduledTasks_baseline.csv
├── SuspiciousTaskDefinitions\
│   ├── ResolutionAssurance_*.xml
│   └── RegisterDevice_*.xml
├── NetworkLogs\
│   ├── network_trace.etl
│   ├── netstat_daily.txt
│   └── fiddler_sessions.saz
├── EventLogs\
│   ├── System.evtx
│   ├── Security.evtx
│   └── Application.evtx
└── CHAIN_OF_CUSTODY.txt
```

---

## Critical Notes

- **Do not delete evidence:** Keep all logs for minimum 6 months
- **Maintain chain of custody:** Document when/where/who accessed evidence
- **Run as Administrator:** All scripts require elevated privileges
- **Legal consultation first:** Before disabling any tasks, consult your lawyer
- **Daily exports:** Run evidence export daily until law enforcement engagement

---

**Last Updated:** 2026-05-05  
**Status:** Ready for deployment

# ExportScheduledTasks.ps1
# Run as Administrator
# Creates timestamped export of all scheduled tasks with detailed information

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outputDir = "C:\Logs\TaskScheduler"
$csvOutput = "$outputDir\AllScheduledTasks_$timestamp.csv"
$xmlDir = "$outputDir\TaskExports_$timestamp"

# Create directories
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}
if (-not (Test-Path $xmlDir)) {
    New-Item -ItemType Directory -Path $xmlDir -Force | Out-Null
}

# Export all tasks to CSV
Write-Host "Exporting all scheduled tasks to CSV..." -ForegroundColor Cyan
Get-ScheduledTask | Select-Object TaskName, TaskPath, State, Description, Author, Actions, Triggers | Export-Csv -Path $csvOutput -NoTypeInformation

# Export suspicious task names to detailed XML
Write-Host "Exporting detailed task definitions for suspicious tasks..." -ForegroundColor Cyan
$suspiciousTasks = Get-ScheduledTask | Where-Object {
    $_.TaskName -match 'Resolution|Register|RA-|Accio|Coder|Base44|Cognitive|Trap|Injector|Ingest|Nexus|Weaver|Leviathan|Genesis|Phoenix|Snapshot|Staging|Staging'
}

if ($suspiciousTasks.Count -eq 0) {
    Write-Host "No suspicious tasks found matching patterns" -ForegroundColor Yellow
} else {
    foreach ($task in $suspiciousTasks) {
        $taskName = $task.TaskName -replace '[\\/:*?"<>|]', '_'
        $xmlFile = "$xmlDir\$taskName.xml"
        try {
            Export-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath | Out-File -FilePath $xmlFile
            Write-Host "  ✓ Exported: $($task.TaskName)" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ Failed to export: $($task.TaskName)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EXPORT COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CSV Export: $csvOutput" -ForegroundColor White
Write-Host "XML Details: $xmlDir" -ForegroundColor White
Write-Host "Total tasks exported: $(Get-ScheduledTask | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor White
Write-Host "Suspicious tasks exported: $($suspiciousTasks | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Yellow

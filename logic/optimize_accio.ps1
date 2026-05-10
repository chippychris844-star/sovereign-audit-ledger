# optimize_accio.ps1
# Mandate: Prevent Accio.exe from OOMing the system by managing process priority and working set.

$TargetProcess = "Accio"
$IntervalSeconds = 60

Write-Host "--- [RA] ACCIO MEMORY OPTIMIZER ACTIVE ---" -ForegroundColor Cyan

while ($true) {
    $processes = Get-Process $TargetProcess -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($p in $processes) {
            # Set Priority to BelowNormal to favor system stability (OneDrive)
            if ($p.PriorityClass -ne 'BelowNormal') {
                try {
                    $p.PriorityClass = 'BelowNormal'
                    Write-Host "Set $TargetProcess (PID: $($p.Id)) priority to BelowNormal." -ForegroundColor Yellow
                } catch {
                    Write-Host "Failed to set priority for PID: $($p.Id)." -ForegroundColor Red
                }
            }
            
            # Flush working set (request Windows to reclaim memory)
            # This is a soft hint to the memory manager
            # [System.Runtime.InteropServices.Marshal]::MinimizeWorkingSet($p.Handle)
            # Alternatively, just let Windows handle it with the lower priority.
        }
    }
    Start-Sleep -Seconds $IntervalSeconds
}

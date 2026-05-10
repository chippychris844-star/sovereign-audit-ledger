param(
  [Parameter(Mandatory=$true)][string]$TargetBat,
  [string]$ShortcutName = "Sovereign RA Engine"
)
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop ($ShortcutName + ".lnk")
$Wsh = New-Object -ComObject WScript.Shell
$Shortcut = $Wsh.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetBat
$Shortcut.WorkingDirectory = Split-Path $TargetBat
$Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,13"
$Shortcut.Description = "Open Sovereign RA Engine"
$Shortcut.Save()
Write-Host "Created $ShortcutPath"

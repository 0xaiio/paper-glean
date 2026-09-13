<#
    Register / remove the Windows Scheduled Task that drives Paper-Glean.

    Defaults: task "PaperGleanDaily", Mon-Sat 11:30, running scripts/run_daily.ps1.

    Usage:
        powershell -NoProfile -ExecutionPolicy Bypass -File scripts/register_task.ps1
        powershell -NoProfile -ExecutionPolicy Bypass -File scripts/register_task.ps1 -Time 09:00
        powershell -NoProfile -ExecutionPolicy Bypass -File scripts/register_task.ps1 -RunNow
        powershell -NoProfile -ExecutionPolicy Bypass -File scripts/register_task.ps1 -Remove

    NOTE: ASCII-only on purpose (see docs/user-guide/scheduling.md).
#>
[CmdletBinding()]
param(
    [string]$TaskName = "PaperGleanDaily",
    [string]$Time = "11:30",
    [string]$Days = "MON,TUE,WED,THU,FRI,SAT",
    [switch]$Remove,
    [switch]$RunNow
)

$ErrorActionPreference = "Stop"

if ($Remove) {
    Write-Host "[INFO] removing scheduled task: $TaskName"
    schtasks /Delete /TN $TaskName /F
    exit $LASTEXITCODE
}

$runner = Join-Path $PSScriptRoot "run_daily.ps1"
if (-not (Test-Path $runner)) {
    Write-Host "[ERR] runner not found: $runner"
    exit 1
}

$action = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$runner`""

Write-Host "[INFO] task    : $TaskName"
Write-Host "[INFO] schedule: WEEKLY on $Days at $Time"
Write-Host "[INFO] action  : $action"

schtasks /Create /TN $TaskName /SC WEEKLY /D $Days /ST $Time /TR $action /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERR] schtasks /Create failed with code $LASTEXITCODE"
    exit $LASTEXITCODE
}

schtasks /Query /TN $TaskName /FO LIST
Write-Host "[OK] registered. Verify with: schtasks /Query /TN $TaskName /V /FO LIST"

if ($RunNow) {
    Write-Host "[INFO] running now..."
    schtasks /Run /TN $TaskName
}

exit 0

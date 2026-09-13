<#
    Paper-Glean daily pipeline - canonical task body.

    Runs: fetch -> digest -> ensure local web app online, then prints artifacts.
    Intended to be invoked by the Windows Scheduled Task created via
    scripts/register_task.ps1 (see docs/user-guide/scheduling.md).

    NOTE: this file is intentionally ASCII-only so it can be read by any
    PowerShell host / code page without corruption.
#>
[CmdletBinding()]
param(
    [int]$Hours = 24,
    [int]$Cap = 100,
    [string]$Date = "",
    [string]$BindHost = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$NoServe
)

$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$py = "python"
if ($env:PAPER_GLEAN_PYTHON) { $py = $env:PAPER_GLEAN_PYTHON }

$cliArgs = @(
    "-X", "utf8", "arxiv_daily.py", "daily",
    "--hours", $Hours,
    "--cap", $Cap,
    "--host", $BindHost,
    "--port", $Port
)
if ($Date) { $cliArgs += @("--date", $Date) }
if (-not $NoServe) { $cliArgs += "--serve" }

Write-Host "[INFO] repo    : $repo"
Write-Host "[INFO] python  : $py"
Write-Host "[INFO] command : $py $($cliArgs -join ' ')"

& $py @cliArgs
$code = $LASTEXITCODE

if ($code -ne 0) {
    Write-Host "[ERR] daily pipeline exited with code $code"
    exit $code
}

Write-Host "[OK] digest : $repo\arXiv-schedule.md"
Write-Host "[OK] records: $repo\data"
exit 0

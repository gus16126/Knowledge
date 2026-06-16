<#
Auto-run helper: waits for a usable `python` on PATH and runs the metadata extractor.
Usage (from PowerShell):
  cd .\.skills\metadata-extractor
  .\auto_run_when_python.ps1 -Topic "two car hauler" -Folders "C:\Users\trans\Documents\Knowledge\Training" "C:\Users\trans\Documents\Knowledge\CarMax Leadership"

Parameters:
  -Topic: topic string to pass to extract_metadata.py
  -Folders: array of folder paths to search
  -IntervalSeconds: how often to check for python (default 5)
  -MaxAttempts: 0 = unlimited
#>
param(
    [string]$Topic = "two car hauler",
    [string[]]$Folders = @("C:\Users\trans\Documents\Knowledge\Training"),
    [int]$IntervalSeconds = 5,
    [int]$MaxAttempts = 0
)

Set-Location -Path $PSScriptRoot
Write-Host "Auto-run extractor helper starting. Topic: '$Topic'" -ForegroundColor Cyan
$attempt = 0
while ($true) {
    $attempt++
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Host "Found python at: $($cmd.Path)" -ForegroundColor Green
        break
    }
    if ($MaxAttempts -gt 0 -and $attempt -ge $MaxAttempts) {
        Write-Error "Timed out waiting for python after $attempt attempts."
        exit 2
    }
    Write-Host "Python not found. Checking again in $IntervalSeconds seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds $IntervalSeconds
}

# Build argument array for the Python process
$scriptPath = Join-Path $PSScriptRoot 'extract_metadata.py'
$procArgs = @($scriptPath, '--topic', $Topic, '--folders') + $Folders

Write-Host "Running extractor: python $($procArgs -join ' ')" -ForegroundColor Cyan
# Invoke python with arguments
& python @procArgs
$exit = $LASTEXITCODE
if ($exit -ne 0) {
    Write-Error "Extractor exited with code $exit"
    exit $exit
}
Write-Host "Extractor finished successfully." -ForegroundColor Green

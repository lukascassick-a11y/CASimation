[CmdletBinding()]
param(
    [switch]$SkipDependencyCheck
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "      CASimation Estimator Launcher" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$pythonCommand = $null
foreach ($candidate in @("py", "python")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $pythonCommand = $candidate
        break
    }
}

if (-not $pythonCommand) {
    Write-Error "Python was not found. Install Python 3.11 or newer, then run this launcher again."
}

$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Creating the local Python environment..." -ForegroundColor Yellow
    & $pythonCommand -m venv .venv
}

if (-not $SkipDependencyCheck) {
    Write-Host "Checking application dependencies..." -ForegroundColor Yellow
    & $venvPython -m pip install --disable-pip-version-check -r requirements.txt
}

Write-Host "Starting CASimation at http://localhost:8501" -ForegroundColor Green
Write-Host "Press Ctrl+C in this window to stop the application." -ForegroundColor DarkGray
Write-Host ""

& $venvPython -m streamlit run app.py --server.address localhost --server.port 8501

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python was not found. Install Python 3.12 or newer."
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".\.venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
python -m streamlit run app.py

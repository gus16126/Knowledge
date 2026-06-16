# Create and activate a Python virtual environment for the metadata extractor.
# Run this from the .skills\metadata-extractor folder in PowerShell.

$venvDir = "venv"
if (-Not (Test-Path $venvDir)) {
    python -m venv $venvDir
}

$activate = Join-Path $venvDir "Scripts\Activate.ps1"
if (-Not (Test-Path $activate)) {
    Write-Error "Virtual environment activation script not found. Ensure Python is installed and venv is available."
    exit 1
}

Write-Host "Activating virtual environment..."
. $activate

if (Test-Path "requirements.txt") {
    Write-Host "Installing requirements..."
    pip install -r requirements.txt
} else {
    Write-Host "No requirements file found; skipping pip install."
}

Write-Host "Virtual environment is ready. Use:\n    .\venv\Scripts\Activate.ps1\n    python extract_metadata.py --topic \"two car hauler\" --folders \"c:\\Users\\trans\\Documents\\Knowledge\\Training\" \"c:\\Users\\trans\\Documents\\Knowledge\\CarMax Leadership\""

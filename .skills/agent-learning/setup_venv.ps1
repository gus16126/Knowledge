# Create and activate a Python virtual environment for the agent-learning tool.
# Run this from the .skills\agent-learning folder in PowerShell.

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

Write-Host "Virtual environment is ready. Use:"
Write-Host "    .\venv\Scripts\Activate.ps1"
Write-Host "    python agent_learning.py log --topic \"python install\" --category environment --tags python install validation --text \"Verify interpreter availability before assuming python works.\""

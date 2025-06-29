# PowerShell script to install Streamlit in virtual environment

# CONFIGURATION
$APP_DIR = "C:\Users\aladi\ClaudeProjects\trading_journal"

# Step 1: Go to project directory
Write-Host "📂 Navigating to project folder..." -ForegroundColor Cyan
Set-Location -Path $APP_DIR

# Step 2: Create a fresh Windows-compatible virtual environment
Write-Host "🧪 Creating a fresh Windows-compatible virtual environment..." -ForegroundColor Cyan

# Backup the old venv if it exists in a non-Windows format
if (Test-Path -Path ".\venv") {
    Write-Host "Found existing virtual environment. Renaming to venv_old..." -ForegroundColor Yellow
    if (Test-Path -Path ".\venv_old") {
        Remove-Item -Recurse -Force ".\venv_old"
    }
    Rename-Item -Path ".\venv" -NewName "venv_old"
}

# Check if Python is available
Write-Host "Checking for Python..." -ForegroundColor Cyan
try {
    python --version
    $pythonCmd = "python"
} catch {
    Write-Host "Python command not found. Checking for py launcher..." -ForegroundColor Yellow
    try {
        py --version
        $pythonCmd = "py"
    } catch {
        Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
        Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
        exit
    }
}

# Create a new venv
Write-Host "Creating new virtual environment..." -ForegroundColor Cyan
& $pythonCmd -m venv venv

# Step 3: Activate the virtual environment
Write-Host "🧪 Activating virtual environment..." -ForegroundColor Cyan
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated." -ForegroundColor Green
} catch {
    Write-Host "❌ Error activating virtual environment. Trying an alternative approach..." -ForegroundColor Yellow
    $env:PATH = "$APP_DIR\venv\Scripts;$env:PATH"
}

# Step 4: Install requirements and streamlit
Write-Host "📦 Installing requirements and Streamlit..." -ForegroundColor Cyan
$pipCmd = ".\venv\Scripts\pip.exe"
if (Test-Path $pipCmd) {
    Write-Host "Using requirements-streamlit.txt..." -ForegroundColor Cyan
    & $pipCmd install -r requirements-streamlit.txt
} else {
    Write-Host "❌ Cannot find pip in the virtual environment. Trying global pip..." -ForegroundColor Yellow
    try {
        $pipCmd = "python -m pip"
        & $pythonCmd -m pip install -r requirements-streamlit.txt
    } catch {
        Write-Host "❌ Failed to install packages. Please install Python and pip correctly." -ForegroundColor Red
        exit
    }
}

Write-Host "✅ Installation complete. You can now run .\launch_streamlit.ps1" -ForegroundColor Green
Write-Host "📝 Note: Your old virtual environment was moved to 'venv_old' folder" -ForegroundColor Yellow

# PowerShell script to find Python installation, set up environment and run Streamlit

# CONFIGURATION
$APP_DIR = "C:\Users\aladi\ClaudeProjects\trading_journal"

# Step 1: Go to project directory
Write-Host "📂 Navigating to project folder..." -ForegroundColor Cyan
Set-Location -Path $APP_DIR

# Step 2: Find Python installation
Write-Host "🔍 Searching for Python 3.13 installation..." -ForegroundColor Cyan

# List of common Python installation paths
$pythonPaths = @(
    # Python 3.13.5 paths
    "C:\Python313\python.exe",
    "C:\Program Files\Python313\python.exe",
    "C:\Program Files\Python\Python313\python.exe",
    "C:\Program Files (x86)\Python313\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
    "C:\Python\Python313\python.exe",
    # More specific Python 3.13.5 paths
    "$env:LOCALAPPDATA\Programs\Python\Python313-64\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python3.13.5\python.exe",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python313\python.exe",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python3.13.5\python.exe",
    # Py launcher path
    "C:\Windows\py.exe"
)

$pythonPath = $null

# Check each path
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $pythonPath = $path
        Write-Host "✅ Found Python at: $pythonPath" -ForegroundColor Green
        break
    }
}

# If not found, try py launcher first
if ($null -eq $pythonPath) {
    Write-Host "Trying py launcher..." -ForegroundColor Yellow
    try {
        $pyVersion = & py -3.13 --version 2>&1
        if ($?) {
            $pythonPath = "py -3.13"
            Write-Host "✅ Using Python via py launcher: $pyVersion" -ForegroundColor Green
        } else {
            throw "Py launcher not available for Python 3.13"
        }
    } catch {
        Write-Host "❌ Python 3.13 not found in common locations or via py launcher." -ForegroundColor Yellow
        $userPath = Read-Host "Please enter the full path to your python.exe"
        
        if (Test-Path $userPath) {
            $pythonPath = $userPath
            Write-Host "✅ Using Python at: $pythonPath" -ForegroundColor Green
        } else {
            Write-Host "❌ Invalid path. Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
            Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
            exit
        }
    }
}

# Step 3: Show Python version
Write-Host "🐍 Python version:" -ForegroundColor Cyan
& $pythonPath --version

# Step 4: Create virtual environment
Write-Host "🧪 Creating virtual environment..." -ForegroundColor Cyan
if ($pythonPath -eq "py -3.13") {
    & py -3.13 -m venv venv
} else {
    & $pythonPath -m venv venv
}

# Step 5: Activate virtual environment
Write-Host "🧪 Activating virtual environment..." -ForegroundColor Cyan
$activateScript = Join-Path $APP_DIR "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✅ Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "❌ Activation script not found. Setting PATH manually..." -ForegroundColor Yellow
    $env:PATH = "$APP_DIR\venv\Scripts;$env:PATH"
}

# Step 6: Install packages
Write-Host "📦 Installing required packages..." -ForegroundColor Cyan
$pipExe = Join-Path $APP_DIR "venv\Scripts\pip.exe"
if (Test-Path $pipExe) {
    & $pipExe install -r requirements.txt
    & $pipExe install streamlit plotly
    Write-Host "✅ Packages installed successfully." -ForegroundColor Green
} else {
    Write-Host "❌ pip.exe not found in virtual environment." -ForegroundColor Red
    exit
}

# Step 7: Run Streamlit
Write-Host "🚀 Starting Streamlit app..." -ForegroundColor Cyan
$pythonExe = Join-Path $APP_DIR "venv\Scripts\python.exe"
if (Test-Path $pythonExe) {
    & $pythonExe -m streamlit run streamlit_app.py
} else {
    Write-Host "❌ python.exe not found in virtual environment." -ForegroundColor Red
    exit
}

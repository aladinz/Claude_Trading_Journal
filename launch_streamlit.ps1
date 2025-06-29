# PowerShell script to run the Streamlit Trading Journal app

# CONFIGURATION
$APP_DIR = "C:\Users\aladi\ClaudeProjects\trading_journal"
$APP_PORT = 5000  # Custom Streamlit port

# Step 1: Go to project directory
Write-Host "📂 Navigating to project folder..." -ForegroundColor Cyan
Set-Location -Path $APP_DIR

# Step 2: Check if virtual environment exists with proper structure
if (Test-Path -Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "🧪 Activating virtual environment..." -ForegroundColor Cyan
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "⚠️ No Windows-compatible virtual environment found." -ForegroundColor Yellow
    Write-Host "Run .\install_streamlit.ps1 first to set up the environment." -ForegroundColor Yellow
    exit
}

# Step 3: Start Streamlit app
Write-Host "🚀 Launching Streamlit app..." -ForegroundColor Cyan
Write-Host "Your app will be available at http://localhost:$APP_PORT" -ForegroundColor Green

try {
    # Try running streamlit from the activated environment
    streamlit run streamlit_app.py --server.port=$APP_PORT
} catch {
    Write-Host "⚠️ Could not run streamlit command. Trying alternative method..." -ForegroundColor Yellow
    try {
        # Try using python -m
        python -m streamlit run streamlit_app.py --server.port=$APP_PORT
    } catch {
        Write-Host "❌ Error: Streamlit failed to run." -ForegroundColor Red
        Write-Host "Running the installer to fix the problem..." -ForegroundColor Yellow
        
        # Run the installer automatically
        & .\install_streamlit.ps1
        
        # Try one more time
        Write-Host "🔄 Trying again after installation..." -ForegroundColor Cyan
        try {
            python -m streamlit run streamlit_app.py --server.port=$APP_PORT
        } catch {
            Write-Host "❌ Final attempt failed. Please check your Python installation and try again." -ForegroundColor Red
        }
    }
}

# The script will continue running until Streamlit is stopped with Ctrl+C

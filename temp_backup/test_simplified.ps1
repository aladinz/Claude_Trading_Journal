# PowerShell script to run the test Streamlit app

Write-Host "🧪 Running simplified test app..." -ForegroundColor Cyan

try {
    # Check if we're in a virtual environment
    $isInVenv = $null -ne $env:VIRTUAL_ENV
    
    if (-not $isInVenv) {
        Write-Host "Not in a virtual environment, activating..." -ForegroundColor Yellow
        if (Test-Path -Path ".\venv\Scripts\Activate.ps1") {
            & .\venv\Scripts\Activate.ps1
        }
    }
    
    # Run the simplified test app
    Write-Host "Running streamlit with minimal test app..." -ForegroundColor Cyan
    streamlit run streamlit_test_basic.py --server.port=5000
} catch {
    Write-Host "❌ Error running simplified test app: $_" -ForegroundColor Red
    Write-Host "Trying Python module approach..." -ForegroundColor Yellow
    
    try {
        python -m streamlit run streamlit_test_basic.py --server.port=5000
    } catch {
        Write-Host "❌ Both methods failed. Error details: $_" -ForegroundColor Red
    }
}

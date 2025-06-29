@echo off
echo Installing and running Streamlit Trading Journal...

:: Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found! Installing or fixing your Python installation...
    echo Please download and install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Create and activate virtual environment if needed
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if activation worked
venv\Scripts\python.exe --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment!
    echo Try running as administrator
    pause
    exit /b 1
)

:: Install requirements
echo Installing requirements...
venv\Scripts\pip.exe install -r requirements.txt
venv\Scripts\pip.exe install streamlit plotly

:: Run streamlit app
echo Starting Streamlit app...
venv\Scripts\python.exe -m streamlit run streamlit_app.py

pause

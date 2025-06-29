@echo off
echo Trading Journal Fresh Install

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe

echo Using Python from: %PYTHON_EXE%

:: Remove existing venv if it exists
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

:: Create a fresh virtual environment
echo Creating a fresh virtual environment...
"%PYTHON_EXE%" -m venv venv

:: Install compatible versions
echo Installing compatible package versions...
call venv\Scripts\activate.bat
venv\Scripts\pip.exe install -r requirements-compatible.txt

:: Run the debug app to check setup
echo Running debug app to verify installation...
venv\Scripts\python.exe -m streamlit run streamlit_debug.py

pause

@echo off
echo Direct Python and Streamlit Install Script

:: Define the location where Python 3.13 is likely installed
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe

echo Looking for Python at: %PYTHON_EXE%

:: Check if Python exists at the expected location
if exist "%PYTHON_EXE%" (
    echo Found Python at %PYTHON_EXE%
) else (
    echo Python not found at the expected location.
    echo Checking other common locations...
    
    for %%p in (
        "C:\Python313\python.exe"
        "C:\Program Files\Python313\python.exe"
        "C:\Program Files\Python\Python313\python.exe"
        "C:\Program Files (x86)\Python313\python.exe"
        "C:\Users\aladi\AppData\Local\Programs\Python\Python313-64\python.exe"
        "C:\Users\aladi\AppData\Local\Programs\Python\Python3.13.5\python.exe"
    ) do (
        if exist %%p (
            set PYTHON_EXE=%%p
            set PYTHON_DIR=%%~dp%%p
            echo Found Python at: %%p
            goto :python_found
        )
    )
    
    echo Python not found in common locations.
    echo Please enter the full path to your python.exe file:
    set /p PYTHON_EXE="> "
    
    if not exist "%PYTHON_EXE%" (
        echo Invalid path. Exiting.
        pause
        exit /b 1
    )
    set PYTHON_DIR=%PYTHON_EXE%\..
)

:python_found
echo Using Python from: %PYTHON_EXE%

:: Create a virtual environment
echo Creating a virtual environment...
"%PYTHON_EXE%" -m venv venv

:: Install packages directly using the full path to pip
echo Installing required packages...
call venv\Scripts\activate.bat
venv\Scripts\pip.exe install -r requirements.txt
venv\Scripts\pip.exe install streamlit plotly

:: Run Streamlit
echo Running Streamlit app...
venv\Scripts\python.exe -m streamlit run streamlit_app.py

pause

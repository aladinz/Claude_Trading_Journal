@echo off
echo Setting up and running Streamlit Trading Journal...

:: Try to find Python in the user's AppData location
set PYTHON_PATH=C:\Users\aladi\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON_PATH%" (
    echo Python not found at expected location: %PYTHON_PATH%
    echo Searching for Python in other locations...
    
    :: Try common locations
    for %%p in (
        "C:\Python313\python.exe"
        "C:\Program Files\Python313\python.exe"
        "C:\Program Files\Python\Python313\python.exe"
        "C:\Program Files (x86)\Python313\python.exe"
        "C:\Users\aladi\AppData\Local\Programs\Python\Python313-64\python.exe"
        "C:\Users\aladi\AppData\Local\Programs\Python\Python3.13.5\python.exe"
    ) do (
        if exist %%p (
            set PYTHON_PATH=%%p
            echo Found Python at: %%p
            goto :python_found
        )
    )
    
    :: Try using py launcher
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo Found py launcher, using it instead
        set USE_PY=1
        goto :python_found
    )
    
    echo Python not found! Please specify the full path to python.exe
    set /p PYTHON_PATH="Enter full path to python.exe: "
    if not exist "%PYTHON_PATH%" (
        echo Invalid path. Exiting.
        pause
        exit /b 1
    )
)

:python_found

:: Create virtual environment
echo Creating virtual environment...
if defined USE_PY (
    py -3.13 -m venv venv
) else (
    "%PYTHON_PATH%" -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo Installing required packages...
venv\Scripts\pip.exe install -r requirements.txt
venv\Scripts\pip.exe install streamlit plotly

:: Run Streamlit app
echo Starting Streamlit app...
venv\Scripts\python.exe -m streamlit run streamlit_app.py

pause

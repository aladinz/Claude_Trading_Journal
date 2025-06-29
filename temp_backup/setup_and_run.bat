@echo off
echo Searching for your Python 3.13 installation...

:: Check common installation locations
set PYTHON_PATHS=^
C:\Python313\python.exe^
C:\Program Files\Python313\python.exe^
C:\Program Files\Python\Python313\python.exe^
C:\Program Files (x86)\Python313\python.exe^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe^
C:\Python\Python313\python.exe

:: Loop through possible paths
for %%p in (%PYTHON_PATHS%) do (
    if exist "%%p" (
        echo Found Python at: %%p
        
        :: Display Python version
        echo Python version:
        "%%p" --version
        
        :: Create virtual environment
        echo.
        echo Creating virtual environment...
        "%%p" -m venv venv
        
        :: Activate virtual environment
        echo.
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
        
        :: Install packages
        echo.
        echo Installing required packages...
        venv\Scripts\pip.exe install -r requirements.txt
        venv\Scripts\pip.exe install streamlit plotly
        
        :: Run the app
        echo.
        echo Starting Streamlit app...
        venv\Scripts\python.exe -m streamlit run streamlit_app.py
        
        goto :found
    )
)

:: If nothing found, prompt the user
echo No Python 3.13 installation was found in the common locations.
echo.
echo Please enter the full path to your python.exe file:
set /p PYTHON_PATH="> "

if exist "%PYTHON_PATH%" (
    echo Using Python at: %PYTHON_PATH%
    
    :: Display Python version
    echo Python version:
    "%PYTHON_PATH%" --version
    
    :: Create virtual environment
    echo.
    echo Creating virtual environment...
    "%PYTHON_PATH%" -m venv venv
    
    :: Activate virtual environment
    echo.
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    :: Install packages
    echo.
    echo Installing required packages...
    venv\Scripts\pip.exe install -r requirements.txt
    venv\Scripts\pip.exe install streamlit plotly
    
    :: Run the app
    echo.
    echo Starting Streamlit app...
    venv\Scripts\python.exe -m streamlit run streamlit_app.py
) else (
    echo The specified path does not exist or is not valid.
    echo Please install Python 3.13 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
)

:found
pause

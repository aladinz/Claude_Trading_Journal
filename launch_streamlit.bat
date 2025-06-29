@echo off
echo Trading Journal Streamlit Launcher

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe

echo Using Python from: %PYTHON_EXE%

:: Create requirements-streamlit.txt if it doesn't exist
if not exist requirements-streamlit.txt (
    echo Creating requirements-streamlit.txt...
    echo streamlit==1.46.1 > requirements-streamlit.txt
    echo plotly==6.2.0 >> requirements-streamlit.txt
    echo pandas==2.3.0 >> requirements-streamlit.txt
    echo numpy==2.3.1 >> requirements-streamlit.txt
    echo altair==5.5.0 >> requirements-streamlit.txt
)

:: Check if venv exists already
if exist "venv\Scripts\activate.bat" (
    echo Using existing virtual environment
) else (
    echo Creating a virtual environment...
    "%PYTHON_EXE%" -m venv venv
    
    echo Installing required packages...
    call venv\Scripts\activate.bat
    venv\Scripts\pip.exe install -r requirements-streamlit.txt
)

:: Activate the virtual environment and run the app
echo Activating virtual environment and starting Streamlit...
call venv\Scripts\activate.bat
venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.port=5185

pause

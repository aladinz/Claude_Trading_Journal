@echo off
echo Streamlit Debug Launcher

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe

echo Using Python from: %PYTHON_EXE%

:: Activate the virtual environment and run the debug app
echo Activating virtual environment and starting Streamlit Debug App...
call venv\Scripts\activate.bat
venv\Scripts\python.exe -m streamlit run streamlit_debug.py

pause

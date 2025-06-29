@echo off
echo Streamlit App - Bypass Onboarding

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe

echo Using Python from: %PYTHON_EXE%

:: Run with fresh start
echo Running Streamlit app...
"%PYTHON_EXE%" -m streamlit run streamlit_app.py --server.headless=true

pause

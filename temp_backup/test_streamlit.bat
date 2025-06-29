@echo off
echo Running Streamlit Test App

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe

echo Using Python from: %PYTHON_EXE%

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run the simplified test app
echo Starting Streamlit test app...
streamlit run streamlit_test.py

pause

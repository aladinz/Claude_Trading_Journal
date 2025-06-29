@echo off
echo Streamlit Latest Version Installer

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set PIP_EXE=%PYTHON_DIR%\Scripts\pip.exe

echo Using Python from: %PYTHON_EXE%
echo Using pip from: %PIP_EXE%

:: First install setuptools
echo Installing setuptools first...
"%PIP_EXE%" install setuptools==68.0.0

:: Install latest compatible packages
echo Installing Streamlit and dependencies...
"%PIP_EXE%" install streamlit
"%PIP_EXE%" install plotly
"%PIP_EXE%" install pandas
"%PIP_EXE%" install altair

:: Create a simple run script without virtual environment
echo @echo off > run_latest.bat
echo echo Running Streamlit with latest version >> run_latest.bat
echo "%PYTHON_EXE%" -m streamlit run streamlit_app.py >> run_latest.bat
echo pause >> run_latest.bat

echo Installation complete. Run the app using run_latest.bat

pause

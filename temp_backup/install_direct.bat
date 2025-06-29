@echo off
echo Direct Streamlit Install - No Virtual Environment

:: Define the Python path that we know works
set PYTHON_DIR=C:\Users\aladi\AppData\Local\Programs\Python\Python313
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set PIP_EXE=%PYTHON_DIR%\Scripts\pip.exe

echo Using Python from: %PYTHON_EXE%
echo Using pip from: %PIP_EXE%

:: Install older compatible versions of packages
echo Installing compatible packages directly...
"%PIP_EXE%" install streamlit==1.28.1 plotly==5.17.0 pandas==1.5.3 numpy==1.24.3 altair==5.1.2

:: Create a simple run script without virtual environment
echo @echo off > run_direct.bat
echo echo Running Streamlit directly with system Python >> run_direct.bat
echo "%PYTHON_EXE%" -m streamlit run streamlit_app.py >> run_direct.bat
echo pause >> run_direct.bat

echo Installation complete. Run the app using run_direct.bat

pause

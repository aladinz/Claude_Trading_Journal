@echo off
REM Run the original Flask Trading Journal application

echo Starting Flask Trading Journal on port 5000...

REM Kill any processes on port 5000 first
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000"') do taskkill /f /pid %%a 2>nul

REM Check if virtual environment exists, if not create it
if not exist "flask_venv" (
    echo Creating Flask virtual environment...
    python -m venv flask_venv
    flask_venv\Scripts\pip.exe install --upgrade pip
    flask_venv\Scripts\pip.exe install Flask SQLAlchemy Flask-SQLAlchemy pandas numpy openpyxl
)

REM Run Flask app
echo Launching Flask app at http://localhost:5000
flask_venv\Scripts\python.exe app.py

echo Flask app stopped.
pause
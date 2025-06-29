@echo off
REM Simple script to run the Streamlit Trading Journal app

echo Starting Trading Journal Streamlit App...

REM Initialize database if needed
if not exist "instance\trading_journal.db" (
    echo Initializing database...
    venv\Scripts\python.exe init_db.py
)

REM Run the Streamlit app locally with custom port
echo Launching Trading Journal locally on port 8504...
set STREAMLIT_SERVER_PORT=8504
venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.port 8504

echo Trading Journal app stopped.
pause
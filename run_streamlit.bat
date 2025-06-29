@echo off
REM Simple script to run the Streamlit Trading Journal app

echo Starting Trading Journal Streamlit App...

REM Initialize database if needed
if not exist "instance\trading_journal.db" (
    echo Initializing database...
    venv\Scripts\python.exe init_db.py
)

REM Run the Streamlit app
echo Launching Streamlit app on port 5185...
venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.port 5185

echo Trading Journal app stopped.
pause
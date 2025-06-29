#!/bin/bash
# Simple script to run the Streamlit Trading Journal app

echo "Starting Trading Journal Streamlit App..."

# Initialize database if needed
if [ ! -f "instance/trading_journal.db" ]; then
    echo "Initializing database..."
    venv/Scripts/python.exe init_db.py
fi

# Run the Streamlit app locally with custom port
echo "Launching Trading Journal locally on port 8504..."
STREAMLIT_SERVER_PORT=8504 venv/Scripts/python.exe -m streamlit run streamlit_app.py --server.port 8504

echo "Trading Journal app stopped."
#!/bin/bash
# Simple script to run the Streamlit Trading Journal app

echo "Starting Trading Journal Streamlit App..."

# Initialize database if needed
if [ ! -f "instance/trading_journal.db" ]; then
    echo "Initializing database..."
    venv/Scripts/python.exe init_db.py
fi

# Run the Streamlit app
echo "Launching Streamlit app on port 5185..."
venv/Scripts/python.exe -m streamlit run streamlit_app.py --server.port 5185

echo "Trading Journal app stopped."
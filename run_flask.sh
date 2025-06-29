#!/bin/bash
# Run the original Flask Trading Journal application

echo "Starting Flask Trading Journal on port 5000..."

# Kill any processes on port 5000 first
lsof -ti:5000 | xargs kill -9 2>/dev/null || true

# Check if virtual environment exists, if not create it
if [ ! -d "flask_venv" ]; then
    echo "Creating Flask virtual environment..."
    python3 -m venv flask_venv
    flask_venv/bin/pip install --upgrade pip
    flask_venv/bin/pip install Flask SQLAlchemy Flask-SQLAlchemy pandas numpy openpyxl
fi

# Run Flask app
echo "Launching Flask app at http://localhost:5000"
flask_venv/bin/python app.py

echo "Flask app stopped."
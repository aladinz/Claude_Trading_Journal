#!/bin/bash

# CONFIGURATION
APP_DIR="/mnt/c/users/aladi/claudeprojects/trading_journal"
APP_COMMAND="python app.py"
APP_PORT=5000
SUBDOMAIN="tradingjournal"   # Optional — pick your custom tunnel name if you want

# Step 1: Go to project directory
echo "📂 Navigating to project folder..."
cd "$APP_DIR"

# Step 2: Activate virtual environment
echo "🧪 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated."

# Step 3: Start Python app in background
echo "🚀 Launching Python app..."
($APP_COMMAND &) 
APP_PID=$!

# Step 4: Wait for app to initialize (you can adjust sleep if needed)
sleep 5

# Step 5: Start LocalTunnel
echo "🌍 Starting LocalTunnel..."
if [ -z "$SUBDOMAIN" ]; then
    lt --port $APP_PORT
else
    lt --port $APP_PORT --subdomain $SUBDOMAIN
fi

# Step 6: After tunnel ends, cleanup
echo "🛑 Stopping Python app..."
kill $APP_PID

echo "✅ All done. Everything shut down cleanly."

#!/bin/bash

# This script is used by the Vercel build process

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements-vercel.txt

# Create the database (optional)
echo "Setting up the database..."
python -c "from app import app; from models import db; app.app_context().push(); db.create_all()"

echo "Build steps completed."
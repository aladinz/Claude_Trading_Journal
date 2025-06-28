#!/bin/bash
echo "Updating database schema for psychological tracking..."
python schema_update.py
echo "Schema update complete! The Trading Journal now includes emotional state tracking."
echo "Restart your Flask application for changes to take effect."
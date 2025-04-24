from flask import Flask
from models import db
from app import app
import os
from sqlalchemy import text

with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    # Add psychological tracking columns if they don't exist yet
    from sqlalchemy import inspect
    
    inspector = inspect(db.engine)
    existing_columns = [column['name'] for column in inspector.get_columns('trade')]
    
    # Define the new columns to add
    new_columns = {
        'entry_emotion': 'VARCHAR(20)',
        'exit_emotion': 'VARCHAR(20)',
        'entry_reason': 'TEXT',
        'exit_reason': 'TEXT',
        'followed_plan': 'BOOLEAN'
    }
    
    # Add each column if it doesn't exist already
    columns_added = False
    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            print(f"Adding column {column_name}...")
            sql = text(f"ALTER TABLE trade ADD COLUMN {column_name} {column_type}")
            with db.engine.connect() as conn:
                conn.execute(sql)
                conn.commit()
            columns_added = True
    
    if columns_added:
        print("Psychological tracking columns added successfully!")
    else:
        print("Schema is already up to date.")
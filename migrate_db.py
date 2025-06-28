from flask import Flask
import sqlite3
from datetime import datetime, timedelta
import os

def migrate_db():
    print("Starting database migration...")
    
    # Connect to the database
    db_path = 'instance/trading_journal.db'
    
    # Make sure the database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file {db_path} not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Backing up existing data...")
    
    # Get all data from the trade table
    cursor.execute("SELECT * FROM trade")
    trades = cursor.fetchall()
    
    # Get column names
    cursor.execute("PRAGMA table_info(trade)")
    columns = [col[1] for col in cursor.fetchall()]
    
    print(f"Found {len(trades)} trades with columns: {columns}")
    
    # Check if we need to migrate
    if 'exit_date' in columns:
        print("Database already migrated, no changes needed.")
        conn.close()
        return
    
    # Create a temporary table with the new schema
    print("Creating new table schema...")
    cursor.execute("""
    CREATE TABLE trade_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TIMESTAMP,
        exit_date TIMESTAMP,
        ticker VARCHAR(10) NOT NULL,
        trade_type VARCHAR(10) NOT NULL,
        entry_price FLOAT NOT NULL,
        exit_price FLOAT,
        shares INTEGER NOT NULL,
        holding_period INTEGER,
        stop_loss FLOAT,
        notes TEXT,
        pl_amount FLOAT,
        pl_percent FLOAT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    """)
    
    # Map columns from old to new
    print("Migrating data to new schema...")
    
    # Find index positions for old columns
    entry_reason_idx = columns.index('entry_reason') if 'entry_reason' in columns else -1
    exit_reason_idx = columns.index('exit_reason') if 'exit_reason' in columns else -1
    date_idx = columns.index('date')
    holding_period_idx = columns.index('holding_period')
    
    # Insert data into the new table
    for trade in trades:
        # Start with base columns excluding entry_reason and exit_reason
        new_values = []
        exit_date = None
        
        for i, col in enumerate(columns):
            # Skip columns we don't want in new schema
            if col in ['entry_reason', 'exit_reason']:
                continue
                
            if col == 'date' and trade[holding_period_idx] is not None:
                # Store the date for calculating exit_date
                entry_date = trade[date_idx]
                new_values.append(entry_date)
                
                # Try to calculate exit_date from date and holding_period
                try:
                    if isinstance(entry_date, str):
                        # Try different date formats
                        try:
                            entry_date_obj = datetime.strptime(entry_date, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                entry_date_obj = datetime.strptime(entry_date, '%Y-%m-%d %H:%M:%S.%f')
                            except ValueError:
                                entry_date_obj = datetime.strptime(entry_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    else:
                        entry_date_obj = datetime.fromtimestamp(entry_date)
                    
                    exit_date = (entry_date_obj + timedelta(days=trade[holding_period_idx])).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    print(f"Error calculating exit date: {e}")
                    exit_date = None
            else:
                new_values.append(trade[i])
        
        # Add exit_date after the date column
        date_pos = 1  # date is the second column (index 1) in the new schema
        new_values.insert(date_pos + 1, exit_date)
        
        # Create placeholders for the SQL query
        placeholders = ", ".join(["?"] * len(new_values))
        
        # Create the INSERT statement
        columns_without_reasons = [c for c in columns if c not in ['entry_reason', 'exit_reason']]
        columns_without_reasons.insert(date_pos + 1, 'exit_date')  # Add exit_date after date
        column_str = ", ".join(columns_without_reasons)
        
        cursor.execute(f"INSERT INTO trade_new ({column_str}) VALUES ({placeholders})", new_values)
    
    print("Replacing old table with new table...")
    cursor.execute("DROP TABLE trade")
    cursor.execute("ALTER TABLE trade_new RENAME TO trade")
    
    # Commit the changes
    conn.commit()
    conn.close()
    
    print("Database migration completed successfully!")

if __name__ == '__main__':
    migrate_db()
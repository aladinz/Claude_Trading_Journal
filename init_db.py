#!/usr/bin/env python3
"""
Database initialization script for Streamlit deployment
Creates the necessary tables and populates with sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_database(db_path):
    """Create database and tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create trades table matching the Flask model structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exit_date TEXT,
            ticker TEXT NOT NULL,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            trade_type TEXT NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL,
            quantity INTEGER NOT NULL,
            shares INTEGER NOT NULL,
            holding_period INTEGER,
            stop_loss REAL,
            notes TEXT,
            profit_loss REAL,
            pnl REAL,
            pl_amount REAL,
            pl_percent REAL,
            strategy TEXT,
            entry_emotion TEXT,
            exit_emotion TEXT,
            entry_reason TEXT,
            exit_reason TEXT,
            followed_plan BOOLEAN,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    return conn

def populate_sample_data(conn):
    """Populate with sample trading data"""
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM trades")
    if cursor.fetchone()[0] > 0:
        print("Database already contains data. Skipping sample data creation.")
        return
    
    # Sample data
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD']
    strategies = ['Day Trade', 'Swing', 'Position', 'Scalp', 'Momentum']
    directions = ['Long', 'Short']
    
    sample_trades = []
    today = datetime.now()
    
    for i in range(20):
        # Random date within last 90 days
        days_ago = random.randint(1, 90)
        trade_date = (today - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        ticker = random.choice(tickers)
        direction = random.choice(directions)
        strategy = random.choice(strategies)
        
        # Generate prices
        base_price = random.uniform(50, 500)
        entry_price = round(base_price, 2)
        
        # 60% win rate
        is_winner = random.random() > 0.4
        price_change = random.uniform(0.02, 0.15)  # 2-15% change
        
        if direction == 'Long':
            if is_winner:
                exit_price = round(entry_price * (1 + price_change), 2)
            else:
                exit_price = round(entry_price * (1 - price_change), 2)
        else:  # Short
            if is_winner:
                exit_price = round(entry_price * (1 - price_change), 2)
            else:
                exit_price = round(entry_price * (1 + price_change), 2)
        
        quantity = random.randint(10, 500)
        
        # Calculate P&L
        if direction == 'Long':
            pnl = (exit_price - entry_price) * quantity
        else:
            pnl = (entry_price - exit_price) * quantity
        
        pnl = round(pnl, 2)
        
        trade_data = (
            trade_date,          # date
            None,                # exit_date
            ticker,              # ticker
            ticker,              # symbol
            direction,           # direction
            'Buy' if direction == 'Long' else 'Sell',  # trade_type
            entry_price,         # entry_price
            exit_price,          # exit_price
            quantity,            # quantity
            quantity,            # shares
            random.randint(1, 15),  # holding_period
            None,                # stop_loss
            None,                # notes
            pnl,                 # profit_loss
            pnl,                 # pnl
            pnl,                 # pl_amount
            round((pnl / (entry_price * quantity)) * 100, 2),  # pl_percent
            strategy,            # strategy
            None,                # entry_emotion
            None,                # exit_emotion
            None,                # entry_reason
            None,                # exit_reason
            None,                # followed_plan
            datetime.now().isoformat(),  # created_at
            datetime.now().isoformat()   # updated_at
        )
        
        sample_trades.append(trade_data)
    
    # Insert sample data
    cursor.executemany('''
        INSERT INTO trades (
            date, exit_date, ticker, symbol, direction, trade_type,
            entry_price, exit_price, quantity, shares, holding_period,
            stop_loss, notes, profit_loss, pnl, pl_amount, pl_percent,
            strategy, entry_emotion, exit_emotion, entry_reason, exit_reason,
            followed_plan, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_trades)
    
    conn.commit()
    print(f"Added {len(sample_trades)} sample trades to database.")

def main():
    """Main initialization function"""
    # Create instance directory if it doesn't exist
    instance_dir = "instance"
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    db_path = os.path.join(instance_dir, "trading_journal.db")
    
    print(f"Initializing database at: {db_path}")
    
    # Create database and tables
    conn = create_database(db_path)
    
    # Populate with sample data
    populate_sample_data(conn)
    
    conn.close()
    print("Database initialization complete!")

if __name__ == "__main__":
    main()
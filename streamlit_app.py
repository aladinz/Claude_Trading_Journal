import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import sqlite3
import random

# Set page config
st.set_page_config(
    page_title="Trading Journal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Connect to the SQLite database
# Detect deployment environment
def get_database_path():
    """Get the appropriate database path based on deployment environment"""
    
    # Check if running on Streamlit Cloud
    if 'STREAMLIT_SHARING' in os.environ or 'STREAMLIT_CLOUD' in os.environ:
        # Use temp directory for Streamlit Cloud
        return "/tmp/trading_journal.db"
    
    # Check other cloud platforms
    if any(key in os.environ for key in ['HEROKU', 'RAILWAY_ENVIRONMENT', 'RENDER']):
        return "/tmp/trading_journal.db"
    
    # Try different database paths for local development
    possible_paths = [
        "instance/trading_journal.db",
        "./instance/trading_journal.db"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Default: create in instance directory
    instance_dir = "instance"
    if not os.path.exists(instance_dir):
        try:
            os.makedirs(instance_dir)
        except:
            # If we can't create instance directory, use temp
            return "/tmp/trading_journal.db"
    
    return "instance/trading_journal.db"

def initialize_database(db_path):
    """Initialize database with schema and sample data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create trades table
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
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM trades")
    if cursor.fetchone()[0] == 0:
        # Add sample data
        populate_sample_data(cursor)
    
    conn.commit()
    conn.close()

def populate_sample_data(cursor):
    """Populate database with sample trading data"""
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

# Get database path and initialize database
@st.cache_resource
def get_database():
    """Get database path and initialize if needed"""
    db_path = get_database_path()
    
    if not os.path.exists(db_path):
        try:
            initialize_database(db_path)
        except Exception as e:
            st.error(f"Database initialization failed: {e}")
            # Return in-memory database as fallback
            return ":memory:"
    
    return db_path

DB_PATH = get_database()

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Function to load trades from database
def load_trades():
    conn = get_db_connection()
    if conn is None:
        st.error("Unable to connect to database.")
        return pd.DataFrame(columns=['date', 'ticker', 'symbol', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl', 'strategy', 'id'])
    
    try:
        # Get data from trades table
        query = "SELECT * FROM trades ORDER BY date DESC"
        trades_df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert date string to datetime object
        if 'date' in trades_df.columns and len(trades_df) > 0:
            trades_df['date'] = pd.to_datetime(trades_df['date'])
        
        # Ensure required columns exist
        required_columns = ['ticker', 'symbol', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl', 'strategy']
        for col in required_columns:
            if col not in trades_df.columns:
                if col == 'symbol':
                    trades_df[col] = trades_df.get('ticker', '')
                elif col == 'quantity':
                    trades_df[col] = trades_df.get('shares', 0)
                elif col == 'pnl':
                    trades_df[col] = trades_df.get('profit_loss', 0.0)
                else:
                    trades_df[col] = None
        
        return trades_df
        
    except Exception as e:
        st.error(f"Error loading trades data: {e}")
        conn.close()
        return pd.DataFrame(columns=['date', 'ticker', 'symbol', 'direction', 'entry_price', 'exit_price', 'quantity', 'pnl', 'strategy', 'id'])

# Sidebar navigation
st.sidebar.title("Trading Journal")
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Trade Journal", "Analytics", "Position Calculator"])

# Load data with error handling
@st.cache_data
def get_trades_data():
    """Load trades data with caching and error handling"""
    try:
        return load_trades()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return sample data as fallback
        return pd.DataFrame({
            'date': pd.date_range(start='2025-01-01', periods=5),
            'ticker': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
            'symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
            'direction': ['Long', 'Short', 'Long', 'Long', 'Short'],
            'entry_price': [150.25, 350.75, 2800.50, 3200.00, 900.50],
            'exit_price': [155.50, 340.25, 2850.75, 3300.00, 850.25],
            'quantity': [10, 5, 2, 3, 15],
            'pnl': [52.50, -52.50, 100.50, 300.00, -753.75],
            'strategy': ['Swing', 'Day Trade', 'Swing', 'Position', 'Day Trade'],
            'id': [1, 2, 3, 4, 5]
        })

try:
    trades_df = get_trades_data()
    has_data = len(trades_df) > 0
    
    if not has_data:
        st.info("No trades found. Using sample data for demonstration.")
except Exception as e:
    st.error(f"Critical error: {e}")
    has_data = False
    trades_df = pd.DataFrame()

# Dashboard Page
if page == "Dashboard":
    st.title("Trading Dashboard")
    
    if has_data:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        col1.metric("Total Trades", total_trades)
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Winning Trades", winning_trades)
        col4.metric("Losing Trades", losing_trades)
        
        # Recent performance
        st.subheader("Recent Performance")
        
        recent_trades = trades_df.head(10)
        if len(recent_trades) > 0:
            fig = px.bar(
                recent_trades,
                x='date',
                y='pnl',
                color=recent_trades['pnl'] > 0,
                color_discrete_map={True: 'green', False: 'red'},
                title="Last 10 Trades PnL"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Monthly performance
        st.subheader("Monthly Performance")
        
        if 'date' in trades_df.columns and len(trades_df) > 0:
            trades_df['month'] = trades_df['date'].dt.strftime('%Y-%m')
            monthly_pnl = trades_df.groupby('month')['pnl'].sum().reset_index()
            
            fig = px.bar(
                monthly_pnl,
                x='month',
                y='pnl',
                color=monthly_pnl['pnl'] > 0,
                color_discrete_map={True: 'green', False: 'red'},
                title="Monthly PnL"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add trades to see your dashboard metrics and charts.")

# Trade Journal Page
elif page == "Trade Journal":
    st.title("Trade Journal")
    
    if has_data:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker_filter = st.multiselect("Filter by Ticker", 
                                         options=sorted(trades_df['ticker'].unique()),
                                         default=[])
        with col2:
            strategy_filter = st.multiselect("Filter by Strategy", 
                                           options=sorted(trades_df['strategy'].unique()),
                                           default=[])
        with col3:
            date_range = st.date_input("Date Range",
                                     value=(trades_df['date'].min(), trades_df['date'].max()) if len(trades_df) > 0 else None,
                                     key="journal_date_filter")
        
        # Apply filters
        filtered_df = trades_df
        if ticker_filter:
            filtered_df = filtered_df[filtered_df['ticker'].isin(ticker_filter)]
        if strategy_filter:
            filtered_df = filtered_df[filtered_df['strategy'].isin(strategy_filter)]
        if date_range and len(date_range) == 2:
            filtered_df = filtered_df[(filtered_df['date'].dt.date >= date_range[0]) & 
                                     (filtered_df['date'].dt.date <= date_range[1])]
        
        # Display trades
        if len(filtered_df) > 0:
            st.dataframe(
                filtered_df.sort_values(by='date', ascending=False),
                use_container_width=True,
                column_config={
                    "pnl": st.column_config.NumberColumn("P&L", format="$%.2f"),
                    "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                }
            )
        else:
            st.info("No trades match your filter criteria.")
    else:
        st.info("No trades found in the database.")

# Analytics Page
elif page == "Analytics":
    st.title("Trading Analytics")
    
    if has_data:
        tab1, tab2, tab3 = st.tabs(["Performance", "Patterns", "Risk Analysis"])
        
        with tab1:
            st.subheader("Performance Metrics")
            
            # Performance by ticker
            ticker_perf = trades_df.groupby('ticker').agg({
                'pnl': ['sum', 'mean', 'count'],
                'id': 'count'
            }).reset_index()
            ticker_perf.columns = ['Ticker', 'Total P&L', 'Avg P&L', 'Win Count', 'Trade Count']
            
            ticker_perf['Win Rate'] = ticker_perf.apply(
                lambda x: f"{(x['Win Count'] / x['Trade Count'] * 100):.1f}%" 
                if x['Trade Count'] > 0 else "0%", axis=1
            )
            
            st.dataframe(
                ticker_perf.sort_values(by='Total P&L', ascending=False),
                use_container_width=True
            )
        
        with tab2:
            st.subheader("Trading Patterns")
            
            # Day of week analysis
            if 'date' in trades_df.columns and len(trades_df) > 0:
                trades_df['day_of_week'] = trades_df['date'].dt.day_name()
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                day_perf = trades_df.groupby('day_of_week').agg({
                    'pnl': ['sum', 'mean', 'count']
                }).reset_index()
                day_perf.columns = ['Day', 'Total P&L', 'Avg P&L', 'Trade Count']
                
                # Reorder days
                day_perf['Day'] = pd.Categorical(day_perf['Day'], categories=day_order, ordered=True)
                day_perf = day_perf.sort_values('Day')
                
                fig = px.bar(
                    day_perf,
                    x='Day',
                    y='Total P&L',
                    color='Total P&L',
                    color_continuous_scale=['red', 'green'],
                    title="P&L by Day of Week"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Risk Analysis")
            
            # Win/Loss ratio
            wins = trades_df[trades_df['pnl'] > 0]
            losses = trades_df[trades_df['pnl'] < 0]
            
            avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
            avg_loss = abs(losses['pnl'].mean()) if len(losses) > 0 else 0
            win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Win", f"${avg_win:.2f}")
            col2.metric("Average Loss", f"${avg_loss:.2f}")
            col3.metric("Win/Loss Ratio", f"{win_loss_ratio:.2f}")
            
            # Drawdown analysis
            if 'date' in trades_df.columns and len(trades_df) > 0:
                trades_df = trades_df.sort_values(by='date')
                trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
                trades_df['running_max'] = trades_df['cumulative_pnl'].cummax()
                trades_df['drawdown'] = trades_df['cumulative_pnl'] - trades_df['running_max']
                
                fig = px.line(
                    trades_df,
                    x='date',
                    y=['cumulative_pnl', 'running_max'],
                    title="Equity Curve with Drawdowns"
                )
                
                # Add drawdown as area
                fig.add_scatter(
                    x=trades_df['date'],
                    y=trades_df['drawdown'],
                    fill='tozeroy',
                    name='Drawdown',
                    line=dict(color='red')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                max_drawdown = abs(trades_df['drawdown'].min())
                st.metric("Maximum Drawdown", f"${max_drawdown:.2f}")
    else:
        st.info("Add trades to see analytics.")

# Position Calculator
elif page == "Position Calculator":
    st.title("Position Size Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        account_size = st.number_input("Account Size ($)", min_value=0.0, value=10000.0, step=1000.0)
        risk_percentage = st.slider("Risk per Trade (%)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        entry_price = st.number_input("Entry Price ($)", min_value=0.01, value=100.0, step=0.01)
        stop_loss = st.number_input("Stop Loss Price ($)", min_value=0.01, value=95.0, step=0.01)
    
    with col2:
        st.subheader("Results")
        
        # Calculate position size
        risk_amount = account_size * (risk_percentage / 100)
        price_difference = abs(entry_price - stop_loss)
        
        if price_difference > 0:
            shares = int(risk_amount / price_difference)
            position_value = shares * entry_price
            actual_risk = shares * price_difference
            actual_risk_percentage = (actual_risk / account_size) * 100
            
            st.metric("Risk Amount", f"${risk_amount:.2f}")
            st.metric("Shares to Trade", shares)
            st.metric("Position Value", f"${position_value:.2f}")
            st.metric("Actual Risk", f"${actual_risk:.2f} ({actual_risk_percentage:.2f}%)")
        else:
            st.error("Entry and stop loss prices must be different.")

# App footer
st.sidebar.markdown("---")
st.sidebar.caption("Trading Journal v1.0")

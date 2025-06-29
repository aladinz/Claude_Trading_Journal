import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import sqlite3
import calendar as cal
from collections import defaultdict

# Set page config
st.set_page_config(
    page_title="Trading Journal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Connect to the SQLite database
# Use different paths for local development vs Streamlit Cloud
if os.path.exists("instance/trading_journal.db"):
    DB_PATH = "instance/trading_journal.db"
elif os.path.exists("./instance/trading_journal.db"):  
    DB_PATH = "./instance/trading_journal.db"
else:
    # Create a fallback in-memory database for demo purposes when deployed
    DB_PATH = ":memory:"
    st.warning("Running in demo mode: Using in-memory database. Your data will not be saved.")

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
        # Return empty DataFrame if connection failed
        st.error("Unable to connect to database. Using sample data.")
        # Create sample data for demo purposes
        sample_data = {
            'date': pd.date_range(start='2025-01-01', periods=5),
            'symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
            'direction': ['Long', 'Short', 'Long', 'Long', 'Short'],
            'entry_price': [150.25, 350.75, 2800.50, 3200.00, 900.50],
            'exit_price': [155.50, 340.25, 2850.75, 3300.00, 850.25],
            'quantity': [10, 5, 2, 3, 15],
            'profit_loss': [52.50, 52.50, 100.50, 300.00, 753.75]
        }
        return pd.DataFrame(sample_data)
    
    try:
        # First check if the trades table exists
        check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='trades'"
        tables = pd.read_sql_query(check_query, conn)
        
        if len(tables) == 0:
            # Table doesn't exist, return empty DataFrame with sample data
            conn.close()
            st.info("No trades table found. Using sample data for demonstration.")
            # Create sample data structure
            sample_data = {
                'date': pd.date_range(start='2025-01-01', periods=5),
                'symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
                'direction': ['Long', 'Short', 'Long', 'Long', 'Short'],
                'entry_price': [150.25, 350.75, 2800.50, 3200.00, 900.50],
                'exit_price': [155.50, 340.25, 2850.75, 3300.00, 850.25],
                'quantity': [10, 5, 2, 3, 15],
                'profit_loss': [52.50, 52.50, 100.50, 300.00, 753.75]
            }
            return pd.DataFrame(sample_data)
        
        # Table exists, get the data
        query = "SELECT * FROM trades ORDER BY date DESC"
        trades_df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert date string to datetime object
        if 'date' in trades_df.columns:
            trades_df['date'] = pd.to_datetime(trades_df['date'])
        
        return trades_df
    except Exception as e:
        st.error(f"Error loading trades data: {e}")
        # Return empty DataFrame with appropriate structure
        return pd.DataFrame(columns=['date', 'symbol', 'direction', 'entry_price', 'exit_price', 'quantity', 'profit_loss'])

# Sidebar navigation
st.sidebar.title("Trading Journal")
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Trade Journal", "Analytics", "Position Calculator"])

# Load data
try:
    trades_df = load_trades()
    if len(trades_df) == 0:
        st.warning("No trades found in the database. Add some trades to get started.")
    has_data = len(trades_df) > 0
except Exception as e:
    st.error(f"Error loading data: {e}")
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

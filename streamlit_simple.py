import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Trading Journal",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def generate_sample_data():
    """Generate sample trading data"""
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    strategies = ['Day Trade', 'Swing', 'Position']
    directions = ['Long', 'Short']
    
    data = []
    today = datetime.now()
    
    for i in range(20):
        days_ago = random.randint(1, 90)
        trade_date = today - timedelta(days=days_ago)
        
        ticker = random.choice(tickers)
        direction = random.choice(directions)
        strategy = random.choice(strategies)
        
        entry_price = round(random.uniform(50, 500), 2)
        is_winner = random.random() > 0.4
        price_change = random.uniform(0.02, 0.15)
        
        if direction == 'Long':
            exit_price = round(entry_price * (1 + price_change if is_winner else 1 - price_change), 2)
        else:
            exit_price = round(entry_price * (1 - price_change if is_winner else 1 + price_change), 2)
        
        quantity = random.randint(10, 500)
        pnl = (exit_price - entry_price) * quantity if direction == 'Long' else (entry_price - exit_price) * quantity
        
        data.append({
            'date': trade_date,
            'ticker': ticker,
            'direction': direction,
            'strategy': strategy,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'quantity': quantity,
            'pnl': round(pnl, 2)
        })
    
    return pd.DataFrame(data)

# Main app
st.title("📊 Trading Journal")

# Load data
trades_df = generate_sample_data()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Dashboard", "Trade Journal"])

if page == "Dashboard":
    st.header("Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['pnl'] > 0])
    total_pnl = trades_df['pnl'].sum()
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    col1.metric("Total Trades", total_trades)
    col2.metric("Win Rate", f"{win_rate:.1f}%")
    col3.metric("Total P&L", f"${total_pnl:.2f}")
    col4.metric("Winning Trades", winning_trades)
    
    # Chart
    st.subheader("Recent Performance")
    chart_data = trades_df.head(10).copy()
    chart_data['color'] = chart_data['pnl'].apply(lambda x: 'Profit' if x > 0 else 'Loss')
    
    st.bar_chart(data=chart_data.set_index('date')['pnl'])

elif page == "Trade Journal":
    st.header("Trade Journal")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        ticker_filter = st.multiselect("Filter by Ticker", options=sorted(trades_df['ticker'].unique()))
    with col2:
        strategy_filter = st.multiselect("Filter by Strategy", options=sorted(trades_df['strategy'].unique()))
    
    # Apply filters
    filtered_df = trades_df
    if ticker_filter:
        filtered_df = filtered_df[filtered_df['ticker'].isin(ticker_filter)]
    if strategy_filter:
        filtered_df = filtered_df[filtered_df['strategy'].isin(strategy_filter)]
    
    # Display trades
    st.dataframe(
        filtered_df.sort_values(by='date', ascending=False),
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.caption("Trading Journal - Streamlit Demo")
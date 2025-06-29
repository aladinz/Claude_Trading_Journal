import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Trading Journal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title  
st.title("📊 Trading Journal")
st.success("✅ Full Trading Journal Application - Version 2.0 Deployed!")
st.info(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Generate sample trading data
@st.cache_data
def load_sample_trades():
    """Generate sample trading data for demonstration"""
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD']
    strategies = ['Day Trade', 'Swing', 'Position', 'Scalp', 'Momentum']
    directions = ['Long', 'Short']
    
    trades = []
    today = datetime.now()
    
    for i in range(20):
        days_ago = random.randint(1, 90)
        trade_date = today - timedelta(days=days_ago)
        
        ticker = random.choice(tickers)
        direction = random.choice(directions)
        strategy = random.choice(strategies)
        
        entry_price = round(random.uniform(50, 500), 2)
        is_winner = random.random() > 0.4  # 60% win rate
        price_change = random.uniform(0.02, 0.15)
        
        if direction == 'Long':
            exit_price = round(entry_price * (1 + price_change if is_winner else 1 - price_change), 2)
        else:
            exit_price = round(entry_price * (1 - price_change if is_winner else 1 + price_change), 2)
        
        quantity = random.randint(10, 500)
        pnl = (exit_price - entry_price) * quantity if direction == 'Long' else (entry_price - exit_price) * quantity
        
        trades.append({
            'date': trade_date,
            'ticker': ticker,
            'symbol': ticker,
            'direction': direction,
            'strategy': strategy,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'quantity': quantity,
            'pnl': round(pnl, 2)
        })
    
    return pd.DataFrame(trades)

# Load data
try:
    trades_df = load_sample_trades()
    has_data = len(trades_df) > 0
except Exception as e:
    st.error(f"Error loading data: {e}")
    has_data = False
    trades_df = pd.DataFrame()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Trade Journal", "Analytics", "Position Calculator"])

# Environment indicator
if 'STREAMLIT_SHARING' in st.session_state or 'STREAMLIT_CLOUD' in st.session_state:
    st.sidebar.success("🌐 Running on Streamlit Cloud")
else:
    st.sidebar.info("🏠 Running with sample data")

if page == "Dashboard":
    st.header("Trading Dashboard")
    
    if has_data:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        total_pnl = trades_df['pnl'].sum()
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        col1.metric("Total Trades", total_trades)
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Total P&L", f"${total_pnl:.2f}")
        col4.metric("Winning Trades", winning_trades)
        
        # Recent performance chart
        st.subheader("Recent Performance")
        recent_trades = trades_df.head(10).copy()
        
        fig = px.bar(
            recent_trades,
            x='date',
            y='pnl',
            color=recent_trades['pnl'] > 0,
            color_discrete_map={True: 'green', False: 'red'},
            title="Last 10 Trades P&L"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly performance
        st.subheader("Monthly Performance")
        trades_df['month'] = trades_df['date'].dt.strftime('%Y-%m')
        monthly_pnl = trades_df.groupby('month')['pnl'].sum().reset_index()
        
        fig2 = px.bar(
            monthly_pnl,
            x='month',
            y='pnl',
            color=monthly_pnl['pnl'] > 0,
            color_discrete_map={True: 'green', False: 'red'},
            title="Monthly P&L"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No trading data available.")

elif page == "Trade Journal":
    st.header("Trade Journal")
    
    if has_data:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            ticker_filter = st.multiselect("Filter by Ticker", 
                                         options=sorted(trades_df['ticker'].unique()),
                                         default=[])
        with col2:
            strategy_filter = st.multiselect("Filter by Strategy", 
                                           options=sorted(trades_df['strategy'].unique()),
                                           default=[])
        
        # Apply filters
        filtered_df = trades_df.copy()
        if ticker_filter:
            filtered_df = filtered_df[filtered_df['ticker'].isin(ticker_filter)]
        if strategy_filter:
            filtered_df = filtered_df[filtered_df['strategy'].isin(strategy_filter)]
        
        # Display trades
        st.dataframe(
            filtered_df.sort_values(by='date', ascending=False),
            use_container_width=True,
            column_config={
                "pnl": st.column_config.NumberColumn("P&L", format="$%.2f"),
                "date": st.column_config.DatetimeColumn("Date", format="YYYY-MM-DD"),
                "entry_price": st.column_config.NumberColumn("Entry Price", format="$%.2f"),
                "exit_price": st.column_config.NumberColumn("Exit Price", format="$%.2f"),
            }
        )
    else:
        st.info("No trading data available.")

elif page == "Analytics":
    st.header("Trading Analytics")
    
    if has_data:
        tab1, tab2 = st.tabs(["Performance", "Risk Analysis"])
        
        with tab1:
            st.subheader("Performance by Ticker")
            perf_by_ticker = trades_df.groupby('ticker').agg({
                'pnl': ['sum', 'mean', 'count']
            }).round(2)
            perf_by_ticker.columns = ['Total P&L', 'Avg P&L', 'Trade Count']
            st.dataframe(perf_by_ticker.sort_values('Total P&L', ascending=False))
            
            # Performance by strategy
            st.subheader("Performance by Strategy")
            perf_by_strategy = trades_df.groupby('strategy').agg({
                'pnl': ['sum', 'mean', 'count']
            }).round(2)
            perf_by_strategy.columns = ['Total P&L', 'Avg P&L', 'Trade Count']
            st.dataframe(perf_by_strategy.sort_values('Total P&L', ascending=False))
        
        with tab2:
            st.subheader("Risk Analysis")
            
            wins = trades_df[trades_df['pnl'] > 0]
            losses = trades_df[trades_df['pnl'] < 0]
            
            avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
            avg_loss = abs(losses['pnl'].mean()) if len(losses) > 0 else 0
            win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Win", f"${avg_win:.2f}")
            col2.metric("Average Loss", f"${avg_loss:.2f}")
            col3.metric("Win/Loss Ratio", f"{win_loss_ratio:.2f}")
    else:
        st.info("No data available for analytics.")

elif page == "Position Calculator":
    st.header("Position Size Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        account_size = st.number_input("Account Size ($)", min_value=0.0, value=10000.0, step=1000.0)
        risk_percentage = st.slider("Risk per Trade (%)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        entry_price = st.number_input("Entry Price ($)", min_value=0.01, value=100.0, step=0.01)
        stop_loss = st.number_input("Stop Loss Price ($)", min_value=0.01, value=95.0, step=0.01)
    
    with col2:
        st.subheader("Results")
        
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

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Trading Journal v2.0 - Streamlit Edition")
st.sidebar.success("🔄 Refresh browser if you see old version")
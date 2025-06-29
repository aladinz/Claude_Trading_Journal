import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Trading Journal",
    page_icon="📊",
    layout="wide"
)

# Page title
st.title("Trading Journal - Simple Test")

# Create some sample data
data = {
    'date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
    'ticker': ['AAPL', 'MSFT', 'AMZN', 'AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AAPL', 'AMZN', 'GOOGL'],
    'strategy': ['Swing', 'Day', 'Swing', 'Day', 'Swing', 'Day', 'Swing', 'Day', 'Swing', 'Day'],
    'pnl': [150, -75, 200, 100, -50, 300, -100, 125, 250, -30]
}

df = pd.DataFrame(data)

# Display basics
st.write("## Data Sample")
st.dataframe(df)

# Simple chart
st.write("## Performance Chart")
fig = px.bar(df, x='date', y='pnl', color='ticker', title="P&L by Date")
st.plotly_chart(fig, use_container_width=True)

# Success message
st.success("Streamlit is working correctly!")

# Version info
st.sidebar.markdown("### Version Info")
st.sidebar.text(f"Streamlit version: {st.__version__}")
st.sidebar.text(f"Pandas version: {pd.__version__}")
st.sidebar.text(f"NumPy version: {np.__version__}")

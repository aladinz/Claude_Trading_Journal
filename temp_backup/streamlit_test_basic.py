import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trading Journal Test", page_icon="✅")

st.title("Trading Journal Test App")
st.write("If you can see this, the app is working correctly!")

# Create some sample data
data = {
    'Date': pd.date_range(start='2025-01-01', periods=5),
    'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
    'Price': [150.25, 350.75, 2800.50, 3200.00, 900.50]
}

df = pd.DataFrame(data)

# Display the data
st.subheader("Sample Trading Data")
st.dataframe(df)

st.success("Everything is working correctly!")

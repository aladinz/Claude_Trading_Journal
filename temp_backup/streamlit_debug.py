import streamlit as st
import sys
import pandas as pd
import sqlite3
import os

st.write("# Streamlit Debug Page")

# System information
st.write("## System Information")
st.write(f"Python version: {sys.version}")
st.write(f"Working directory: {os.getcwd()}")

# Check package versions
st.write("## Package Versions")
import pkg_resources
packages = ['streamlit', 'pandas', 'numpy', 'plotly', 'altair']
for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        st.write(f"{package}: {version}")
    except pkg_resources.DistributionNotFound:
        st.write(f"{package}: Not found")

# Check database connection
st.write("## Database Check")
DB_PATH = "instance/trading_journal.db"

if os.path.exists(DB_PATH):
    st.write(f"Database file exists: {DB_PATH}")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        st.write("Tables in database:")
        for table in tables:
            st.write(f"- {table[0]}")
            
        # Sample data from trades table if it exists
        if any(table[0] == 'trades' for table in tables):
            st.write("### Sample data from trades table:")
            cursor.execute("SELECT * FROM trades LIMIT 5")
            columns = [description[0] for description in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            st.dataframe(df)
        
        conn.close()
        st.write("✅ Database connection successful")
    except Exception as e:
        st.write(f"❌ Database error: {str(e)}")
else:
    st.write(f"❌ Database file not found: {DB_PATH}")

st.write("## Test Complete")
st.write("If you see this, Streamlit is running correctly!")

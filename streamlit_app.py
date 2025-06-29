import streamlit as st
import sys
import os

# Display system info for debugging
st.title("🩺 Streamlit Health Check")

st.success("✅ Streamlit is running!")

# System information
st.subheader("System Information")
st.write(f"Python version: {sys.version}")
st.write(f"Current working directory: {os.getcwd()}")
st.write(f"Python path: {sys.executable}")

# Environment variables
st.subheader("Environment Check")
env_vars = ['STREAMLIT_SHARING', 'STREAMLIT_CLOUD', 'PORT', 'PYTHONPATH']
for var in env_vars:
    value = os.environ.get(var, 'Not set')
    st.write(f"{var}: {value}")

# Test basic Streamlit components
st.subheader("Component Test")
st.write("Basic text: ✅")
st.button("Test button")
st.slider("Test slider", 0, 100, 50)

st.info("If you can see this page, Streamlit is working correctly!")
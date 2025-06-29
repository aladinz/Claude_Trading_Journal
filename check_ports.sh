#!/bin/bash
# Check what's running on trading journal ports

echo "=== Trading Journal Applications Status ==="
echo ""

echo "Port 5000 (Flask App - Original):"
ss -tulpn | grep :5000 || echo "  - Available"
echo ""

echo "Port 8504 (Streamlit App - Local):"
ss -tulpn | grep :8504 || echo "  - Available"
echo ""

echo "Port 8501 (Streamlit Cloud):"
ss -tulpn | grep :8501 || echo "  - Available"
echo ""

echo "Running processes:"
echo "Flask processes:"
ps aux | grep "python.*app.py" | grep -v grep || echo "  - None found"
echo ""
echo "Streamlit processes:"
ps aux | grep streamlit | grep -v grep || echo "  - None found"
echo ""

echo "=== How to start applications ==="
echo ""
echo "Original Flask Trading Journal (port 5000):"
echo "  ./run_flask.sh"
echo "  OR manually: flask_venv/bin/python app.py"
echo ""
echo "Streamlit Trading Journal (port 8504 local):"
echo "  ./run_streamlit.sh"
echo "  OR manually: venv/Scripts/python.exe -m streamlit run streamlit_app.py --server.port 8504"
# Streamlit Deployment Guide

## Fixed Dependency Issues

### Changes Made:
1. **Updated requirements.txt** - Set compatible package versions
2. **Updated runtime.txt** - Changed to Python 3.11 for better compatibility  
3. **Enhanced deployment detection** - App now automatically detects cloud environments
4. **Added packages.txt** - System packages for build process

### Files for Deployment:
- `requirements.txt` - Core Python dependencies with compatible versions
- `runtime.txt` - Python version specification
- `packages.txt` - System packages needed for deployment
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml` - Secrets configuration (empty template)

### Key Dependency Versions:
```
streamlit==1.28.0
pandas==1.5.3
numpy==1.24.3
plotly==5.15.0
altair==4.2.2
```

### Deployment Steps:
1. **Push updated files** - Make sure all files are committed
2. **Redeploy** - Trigger a new deployment on your platform
3. **Check logs** - Monitor deployment for any remaining issues

### Environment Detection:
The app automatically detects:
- Streamlit Cloud (`STREAMLIT_SHARING`, `STREAMLIT_CLOUD`)
- Heroku (`HEROKU`)
- Railway (`RAILWAY_ENVIRONMENT`) 
- Render (`RENDER`)

### Database Handling:
- **Local**: Uses `instance/trading_journal.db`
- **Cloud**: Uses `/tmp/trading_journal.db` with auto-initialization

### Port Configuration:
- **Cloud deployment**: Port 8501 (for health checks)
- **Local development**: Port 8504 (to avoid conflicts)
- **Configuration files**:
  - `.streamlit/config.toml` - Cloud deployment (8501)
  - `.streamlit/config_local.toml` - Local development (8504)

### Running the App:
- **Cloud**: Automatically uses port 8501
- **Local**: Use `./run_streamlit.sh` for port 8504
- **Manual local**: `venv/Scripts/python.exe -m streamlit run streamlit_app.py --server.port 8504`

### Environment Detection:
The app displays:
- 🌐 "Running on Streamlit Cloud" when deployed
- 🏠 "Running locally" when running locally

The dependency error should now be resolved with these compatible package versions.
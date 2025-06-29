# Port Configuration Notes

## Local Development
When running the app locally using the provided scripts, the app will use port 8501 (Streamlit default).

## Deployment
For deployment to platforms like Streamlit Cloud:
- The platform will automatically assign the appropriate port
- No need to specify port in the configuration
- Health checks will occur on port 8501 by default

## Custom Port Configuration
If you need to use a custom port locally:
1. Update the port in `.streamlit/config.toml`
2. Update the port in launch scripts (`launch_streamlit.bat` and `launch_streamlit.ps1`)
3. Use the `--server.port=XXXX` flag when running Streamlit directly

Note that most deployment platforms will override these settings with their own port configuration.

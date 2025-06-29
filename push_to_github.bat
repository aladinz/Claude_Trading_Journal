@echo off
echo Pushing streamlit_app.py to GitHub repository

:: Navigate to the project directory
cd /d C:\Users\aladi\ClaudeProjects\trading_journal

echo Current directory: %CD%

:: Check if git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git is not installed or not in the PATH
    echo Please install Git from https://git-scm.com/downloads
    pause
    exit /b 1
)

:: Check if the directory is a git repository
if not exist .git (
    echo Initializing git repository...
    git init
    
    echo Adding remote origin...
    git remote add origin https://github.com/aladinz/Claude_Trading_Journal.git
)

:: Add all necessary files to staging
git add streamlit_app.py
git add requirements.txt
git add requirements-streamlit.txt
git add launch_streamlit.bat
git add launch_streamlit.ps1
git add install_streamlit.ps1
git add .streamlit/config.toml
git add cleanup.bat
git add README.md
git add debug_streamlit.bat
git add streamlit_debug.py
git add streamlit_test.py

:: Create a requirements-streamlit.txt file if it doesn't exist
if not exist requirements-streamlit.txt (
    echo Creating Streamlit requirements file...
    echo streamlit==1.46.1 > requirements-streamlit.txt
    echo plotly==6.2.0 >> requirements-streamlit.txt
    echo pandas==2.3.0 >> requirements-streamlit.txt
    echo numpy==2.3.1 >> requirements-streamlit.txt
    git add requirements-streamlit.txt
)

:: Commit the changes
git commit -m "Update Streamlit port to 5185"

:: Push to GitHub
echo Pushing to GitHub repository...
git push -u origin master

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo If you encountered an error, it may be because:
    echo 1. You need to authenticate with GitHub
    echo 2. The remote branch name is 'main' instead of 'master'
    echo 3. There are conflicts with the remote repository
    echo.
    echo Trying with 'main' branch instead...
    git push -u origin master:main
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Alternative push methods:
        echo - Try forcing the push: git push -f origin master:main
        echo - Or create a new branch: git checkout -b streamlit-app ^&^& git push -u origin streamlit-app
    )
)

echo.
echo Done! Check your GitHub repository at:
echo https://github.com/aladinz/Claude_Trading_Journal
echo.
pause

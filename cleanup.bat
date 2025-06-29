@echo off
echo Cleaning up temporary and unnecessary files...

cd /d C:\Users\aladi\ClaudeProjects\trading_journal

:: List of files to be deleted (temporary and redundant files)
set FILES_TO_DELETE=^
find_python_and_run.ps1^
direct_install.bat^
setup_streamlit.bat^
install_streamlit.ps1^
setup_and_run.bat^
__pycache__^
.vercel^
.venv

:: Temp directory to move files instead of deleting directly
if not exist temp_backup mkdir temp_backup

:: Move each file to backup before deletion
echo Moving files to temporary backup...
for %%f in (%FILES_TO_DELETE%) do (
    if exist %%f (
        echo - %%f
        if exist %%f\* (
            :: It's a directory
            mkdir temp_backup\%%f 2>nul
            xcopy /s /e /y %%f temp_backup\%%f >nul
            rd /s /q %%f
        ) else (
            :: It's a file
            copy %%f temp_backup\ >nul
            del %%f
        )
    )
)

:: Keep only essential files for the project
echo.
echo The following essential files have been kept:
echo - streamlit_app.py (Streamlit application)
echo - app.py (Flask application)
echo - launch_streamlit.bat (Streamlit launcher)
echo - requirements.txt (Project dependencies)
echo - push_to_github.bat (GitHub push script)
echo - models/ (Data models)
echo - templates/ (HTML templates)
echo - static/ (Static assets)
echo - README.md (Documentation)

echo.
echo Cleanup complete!
echo If you need any of the removed files, they are in the temp_backup directory.
echo You can safely delete the temp_backup directory if everything works as expected.
echo.
pause

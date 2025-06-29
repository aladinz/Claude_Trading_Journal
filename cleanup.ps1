# PowerShell script to clean up unnecessary files
$projectDir = "C:\Users\aladi\ClaudeProjects\trading_journal"
Set-Location -Path $projectDir

# Create backup directory if it doesn't exist
$backupDir = Join-Path -Path $projectDir -ChildPath "temp_backup"
if (-not (Test-Path -Path $backupDir)) {
    New-Item -Path $backupDir -ItemType Directory | Out-Null
    Write-Host "Created backup directory: $backupDir" -ForegroundColor Yellow
}

# List of files to be moved to backup
$filesToCleanup = @(
    "find_python_and_run.ps1",
    "direct_install.bat",
    "setup_streamlit.bat",
    "setup_and_run.bat",
    "test_simplified.ps1",
    "streamlit_test.py",
    "streamlit_test_basic.py",
    "streamlit_debug.py",
    "debug_streamlit.bat",
    "fresh_install.bat",
    "run_direct.bat",
    "run_headless.bat",
    "run_latest.bat",
    "install_direct.bat",
    "install_latest.bat",
    "test_streamlit.bat",
    "run_streamlit.bat",
    "minimal_test.py",
    "requirements_minimal.txt",
    "requirements-compatible.txt",
    "requirements-vercel.txt"
)

# Move files to backup
Write-Host "Moving files to backup directory..." -ForegroundColor Cyan
foreach ($file in $filesToCleanup) {
    $filePath = Join-Path -Path $projectDir -ChildPath $file
    if (Test-Path -Path $filePath) {
        $destPath = Join-Path -Path $backupDir -ChildPath $file
        Move-Item -Path $filePath -Destination $destPath -Force
        Write-Host "  - Moved: $file" -ForegroundColor Green
    }
}

# List of folders to backup
$foldersToBackup = @(
    "__pycache__",
    "venv_old"
)

# Move folders to backup
foreach ($folder in $foldersToBackup) {
    $folderPath = Join-Path -Path $projectDir -ChildPath $folder
    if (Test-Path -Path $folderPath) {
        $destPath = Join-Path -Path $backupDir -ChildPath $folder
        if (-not (Test-Path -Path $destPath)) {
            New-Item -Path $destPath -ItemType Directory | Out-Null
        }
        
        # Copy contents then remove original
        Copy-Item -Path "$folderPath\*" -Destination $destPath -Recurse -Force
        Remove-Item -Path $folderPath -Recurse -Force
        Write-Host "  - Backed up folder: $folder" -ForegroundColor Green
    }
}

# List essential files that remain
Write-Host "`nThe following essential files have been kept:" -ForegroundColor Cyan
$essentialFiles = @(
    "streamlit_app.py (Streamlit application)",
    "app.py (Flask application)",
    "launch_streamlit.bat (Windows batch launcher)",
    "launch_streamlit.ps1 (PowerShell launcher)",
    "requirements.txt (Project dependencies for cloud deployment)",
    "requirements-streamlit.txt (Streamlit-specific dependencies)",
    ".streamlit/config.toml (Streamlit configuration)",
    "push_to_github.bat (GitHub push script)",
    "models/ (Data models)",
    "templates/ (HTML templates)",
    "static/ (Static assets)",
    "README.md (Documentation)",
    "LICENSE (License file)"
)

foreach ($file in $essentialFiles) {
    Write-Host "  - $file" -ForegroundColor Green
}

Write-Host "`nCleanup complete!" -ForegroundColor Cyan
Write-Host "If you need any of the backed up files, they are in the temp_backup directory." -ForegroundColor Yellow
Write-Host "You can safely delete the temp_backup directory if everything works as expected." -ForegroundColor Yellow

# Pause to see the output
Write-Host "`nPress Enter to continue..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

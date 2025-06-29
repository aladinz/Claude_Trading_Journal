# PowerShell script to fix the specific Git errors
Write-Host "Git Error Fix Helper" -ForegroundColor Cyan
Write-Host "==================\n" -ForegroundColor Cyan

# Step 1: Make sure flask_venv is ignored
Write-Host "Step 1: Ensuring flask_venv is excluded from Git tracking..." -ForegroundColor Yellow
if (Test-Path -Path ".git/info/exclude") {
    Add-Content -Path ".git/info/exclude" -Value "flask_venv/"
    Add-Content -Path ".git/info/exclude" -Value "flask_venv/bin/python"
    Write-Host "  Added flask_venv to local Git exclude file" -ForegroundColor Green
}

# Step 2: Remove any tracked flask_venv files from the index
Write-Host "`nStep 2: Attempting to remove flask_venv from Git index..." -ForegroundColor Yellow
git rm --cached -r flask_venv 2>$null
Write-Host "  (Errors can be ignored if files weren't previously tracked)" -ForegroundColor Gray

# Step 3: Add only necessary files
Write-Host "`nStep 3: Adding only necessary files to commit..." -ForegroundColor Yellow
Write-Host "  Adding modified files (excluding flask_venv)..." -ForegroundColor Gray
git add .gitignore
git add run_streamlit.bat
git add run_streamlit.sh
git add runtime.txt
git add STREAMLIT_DEPLOYMENT.md
git add check_ports.sh
git add requirements-flask.txt
git add run_flask.bat
git add run_flask.sh
git add streamlit_app_backup.py
git add streamlit_simple.py

# Step 4: Show what's being committed
Write-Host "`nStep 4: Files staged for commit:" -ForegroundColor Yellow
git status

# Step 5: Confirm and commit
Write-Host "`nStep 5: Ready to commit these changes?" -ForegroundColor Yellow
$confirmation = Read-Host "Type 'yes' to commit or anything else to cancel"

if ($confirmation -eq "yes") {
    $commitMessage = Read-Host "Enter commit message"
    git commit -m $commitMessage
    Write-Host "`nChanges committed successfully!" -ForegroundColor Green
    
    # Ask about pushing
    $pushConfirmation = Read-Host "Push changes to remote repository? (yes/no)"
    if ($pushConfirmation -eq "yes") {
        git push
        Write-Host "Changes pushed to remote repository." -ForegroundColor Green
    }
} else {
    Write-Host "`nCommit cancelled." -ForegroundColor Yellow
}

# PowerShell script to safely commit files to Git
Write-Host "Safe Git Commit Helper" -ForegroundColor Cyan
Write-Host "====================\n" -ForegroundColor Cyan

# Step 1: Reset the Git index to clean state
Write-Host "Step 1: Resetting Git index..." -ForegroundColor Yellow
git reset

# Step 2: Add specific file types, avoiding binaries and virtual environments
Write-Host "`nStep 2: Adding specific file types safely..." -ForegroundColor Yellow
git add *.py *.md *.txt *.html *.css *.js *.json *.bat *.ps1 *.sh .streamlit/ models/ static/ templates/

# Step 3: Show what's being committed
Write-Host "`nStep 3: Files staged for commit:" -ForegroundColor Yellow
git status

# Step 4: Confirm and commit
Write-Host "`nStep 4: Ready to commit these changes?" -ForegroundColor Yellow
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

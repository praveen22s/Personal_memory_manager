# Push to GitHub Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Push to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if remote exists
$remoteUrl = git remote get-url origin 2>$null

if ($remoteUrl) {
    Write-Host "[OK] Remote found: $remoteUrl" -ForegroundColor Green
    Write-Host ""
    
    # Check current branch
    $branch = git branch --show-current
    Write-Host "Current branch: $branch" -ForegroundColor Cyan
    
    if ($branch -ne "main") {
        Write-Host "Renaming branch to main..." -ForegroundColor Yellow
        git branch -M main
    }
    
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    Write-Host ""
    
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[SUCCESS] Pushed to GitHub!" -ForegroundColor Green
        Write-Host "Repository: $remoteUrl" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "[ERROR] Push failed!" -ForegroundColor Red
        Write-Host "Common issues:" -ForegroundColor Yellow
        Write-Host "1. Authentication required (use Personal Access Token)"
        Write-Host "2. Repository doesn't exist on GitHub yet"
        Write-Host "3. Check your internet connection"
    }
} else {
    Write-Host "[ERROR] No remote repository configured!" -ForegroundColor Red
    Write-Host ""
    Write-Host "First, create a repository on GitHub, then run:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  git remote add origin https://github.com/USERNAME/REPO.git" -ForegroundColor White
    Write-Host "  git branch -M main" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "Or run: .\setup_github.ps1" -ForegroundColor Yellow
}

Write-Host ""

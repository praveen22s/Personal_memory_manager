# GitHub Setup Script for Personal Semantic Diary

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Setup Wizard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "[OK] Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win"
    exit 1
}

Write-Host ""

# Check if already a git repository
if (Test-Path .git) {
    Write-Host "[INFO] Git repository already initialized" -ForegroundColor Yellow
    $reinit = Read-Host "Do you want to re-initialize? (y/N)"
    if ($reinit -eq 'y' -or $reinit -eq 'Y') {
        Remove-Item -Recurse -Force .git
        Write-Host "[OK] Removed existing .git directory" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Keeping existing repository" -ForegroundColor Yellow
    }
}

# Initialize git if needed
if (-not (Test-Path .git)) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Staging all files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to commit!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit: Personal Semantic Diary - AI-powered diary with semantic graph storage"
}

Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Commit created successfully!" -ForegroundColor Green
} else {
    Write-Host "[WARN] Commit may have failed or nothing to commit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://github.com and create a new repository" -ForegroundColor White
Write-Host "2. Copy the repository URL (e.g., https://github.com/USERNAME/REPO.git)" -ForegroundColor White
Write-Host "3. Run the following commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin YOUR_REPO_URL" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or run:" -ForegroundColor White
Write-Host "   .\push_to_github.ps1" -ForegroundColor Yellow
Write-Host ""

$setupRemote = Read-Host "Do you want to set up remote now? (y/N)"
if ($setupRemote -eq 'y' -or $setupRemote -eq 'Y') {
    $repoUrl = Read-Host "Enter your GitHub repository URL"
    if ($repoUrl) {
        Write-Host ""
        Write-Host "Adding remote..." -ForegroundColor Yellow
        git remote add origin $repoUrl 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Remote added: $repoUrl" -ForegroundColor Green
            
            Write-Host ""
            Write-Host "Renaming branch to main..." -ForegroundColor Yellow
            git branch -M main
            
            Write-Host ""
            Write-Host "[OK] Ready to push!" -ForegroundColor Green
            Write-Host "Run: git push -u origin main" -ForegroundColor Yellow
        } else {
            Write-Host "[WARN] Remote may already exist" -ForegroundColor Yellow
            Write-Host "To update: git remote set-url origin $repoUrl" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "Done! Check GITHUB_SETUP.md for detailed instructions." -ForegroundColor Green

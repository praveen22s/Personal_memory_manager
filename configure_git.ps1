# Configure Git User

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Git Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$email = Read-Host "Enter your email address (for Git commits)"
$name = Read-Host "Enter your name (for Git commits)"

if ($email -and $name) {
    Write-Host ""
    Write-Host "Configuring Git..." -ForegroundColor Yellow
    git config --global user.email $email
    git config --global user.name $name
    
    Write-Host "[OK] Git configured!" -ForegroundColor Green
    Write-Host "Email: $email" -ForegroundColor Cyan
    Write-Host "Name: $name" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Now run: .\setup_github.ps1" -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Email and name are required!" -ForegroundColor Red
}

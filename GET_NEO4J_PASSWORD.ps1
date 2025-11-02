# Helper script to guide finding Neo4j password

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Neo4j Password Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Steps to find your Neo4j password:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open Neo4j Desktop 2" -ForegroundColor White
Write-Host "2. Click on your database in the left sidebar" -ForegroundColor White
Write-Host "3. Look at the Details panel (right side)" -ForegroundColor White
Write-Host "4. Find the Password field" -ForegroundColor White
Write-Host "5. Click the 'Show' button or eye icon to reveal password" -ForegroundColor White
Write-Host ""
Write-Host "Alternative:" -ForegroundColor Yellow
Write-Host "- Click 'Open' button next to your database" -ForegroundColor White
Write-Host "- Browser opens at http://localhost:7474" -ForegroundColor White
Write-Host "- Try logging in with username 'neo4j'" -ForegroundColor White
Write-Host "- Use the password that works there!" -ForegroundColor White
Write-Host ""

$password = Read-Host "Enter your Neo4j password (or press Enter to skip)"

if ([string]::IsNullOrWhiteSpace($password)) {
    Write-Host ""
    Write-Host "[INFO] You can update password later using: .\UPDATE_PASSWORD.ps1" -ForegroundColor Yellow
    Write-Host "Or manually edit .env file" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To open .env file, run:" -ForegroundColor Cyan
    Write-Host "  notepad .env" -ForegroundColor White
    Write-Host ""
    exit 0
}

# Update .env
if (Test-Path .env) {
    $envContent = Get-Content .env
    $updated = $false
    $newContent = @()
    
    foreach ($line in $envContent) {
        if ($line -match "^NEO4J_PASSWORD=(.+)") {
            $newContent += "NEO4J_PASSWORD=$password"
            $updated = $true
        } else {
            $newContent += $line
        }
    }
    
    if ($updated) {
        $newContent | Set-Content .env
        Write-Host ""
        Write-Host "[OK] Password updated in .env file!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Testing connection..." -ForegroundColor Yellow
        python test_connection.py
    } else {
        Write-Host "[ERROR] Could not find NEO4J_PASSWORD in .env" -ForegroundColor Red
    }
} else {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env -ErrorAction SilentlyContinue
    Write-Host "[OK] Created .env - Please run this script again" -ForegroundColor Green
}

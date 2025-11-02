# Neo4j Connection Helper Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Neo4j Connection Checker" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Neo4j is running
Write-Host "Checking if Neo4j is running on port 7687..." -ForegroundColor Yellow
$result = Test-NetConnection -ComputerName localhost -Port 7687 -InformationLevel Quiet -WarningAction SilentlyContinue

if ($result) {
    Write-Host "[OK] Neo4j is running on localhost:7687" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Neo4j is NOT running!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "1. Open Neo4j Desktop" -ForegroundColor White
    Write-Host "2. Start your database (click the play button)" -ForegroundColor White
    Write-Host "3. Wait for it to show 'Active'" -ForegroundColor White
    exit 1
}

Write-Host ""

# Check .env file
Write-Host "Checking .env file..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
    Write-Host ""
    
    # Read and display settings (mask password)
    $envContent = Get-Content .env
    $envContent | ForEach-Object {
        if ($_ -match "NEO4J_PASSWORD=(.+)") {
            Write-Host "NEO4J_PASSWORD=***hidden***" -ForegroundColor Gray
        } else {
            Write-Host $_ -ForegroundColor Gray
        }
    }
} else {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "Creating from .env.example..." -ForegroundColor Yellow
    
    Copy-Item .env.example .env -ErrorAction SilentlyContinue
    Write-Host "[OK] Created .env - Please edit it with your Neo4j password" -ForegroundColor Green
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next: Run 'python test_connection.py'" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan


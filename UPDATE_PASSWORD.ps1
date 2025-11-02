# Quick Neo4j Password Updater

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Update Neo4j Password" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$newPassword = Read-Host "Enter your Neo4j database password"

if ([string]::IsNullOrWhiteSpace($newPassword)) {
    Write-Host "[ERROR] Password cannot be empty!" -ForegroundColor Red
    exit 1
}

# Update .env file
$envContent = Get-Content .env
$updated = $false
$newContent = @()

foreach ($line in $envContent) {
    if ($line -match "^NEO4J_PASSWORD=(.+)") {
        $newContent += "NEO4J_PASSWORD=$newPassword"
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
    Write-Host ""
    
    # Test the connection
    python test_connection.py
    
} else {
    Write-Host "[ERROR] Could not find NEO4J_PASSWORD in .env file" -ForegroundColor Red
    exit 1
}


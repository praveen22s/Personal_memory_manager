# Start Frontend Server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Frontend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

cd frontend

Write-Host "Running: npm run dev" -ForegroundColor Yellow
Write-Host ""
Write-Host "The frontend will open at:" -ForegroundColor Green
Write-Host "http://localhost:5173" -ForegroundColor White
Write-Host ""

npm run dev

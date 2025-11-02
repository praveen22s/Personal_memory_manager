@echo off
echo Starting Personal Semantic Diary...
echo.

echo [1/2] Starting Backend Server...
start cmd /k "python main.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause >nul





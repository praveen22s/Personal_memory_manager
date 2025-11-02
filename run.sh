#!/bin/bash

echo "Starting Personal Semantic Diary..."
echo ""

echo "[1/2] Starting Backend Server..."
python3 main.py &
BACKEND_PID=$!

sleep 3

echo "[2/2] Starting Frontend Server..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "Both servers are running..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

wait $BACKEND_PID $FRONTEND_PID





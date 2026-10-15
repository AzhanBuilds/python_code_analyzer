@echo off
echo Starting Python Code Analyzer (Backend + Frontend)...
cd /d "%~dp0"

start "Python Analyzer - Backend" cmd /k "python backend\app.py"
start "Python Analyzer - Frontend" cmd /k "cd frontend && npm.cmd run dev"

echo.
echo ==============================================
echo Python Code Analyzer started!
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo ==============================================
echo.

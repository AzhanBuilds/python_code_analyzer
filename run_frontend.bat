@echo off
echo Starting Python Code Analyzer Frontend (Vite)...
cd /d "%~dp0frontend"
call npm.cmd run dev
pause

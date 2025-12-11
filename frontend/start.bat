@echo off
REM Quick Start Script for Frontend
REM This script sets up and starts the Flask frontend

echo ========================================
echo   Text Analysis Frontend - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install/Update dependencies using UV
echo Installing dependencies with UV...
pip install uv
uv pip install -e .
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env > nul
    echo.
    echo IMPORTANT: Please edit .env and set your backend URL!
    echo Default is set to: http://localhost:8000
    echo.
    timeout /t 3 > nul
)

REM Check if backend is running
echo Checking backend connection...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Backend doesn't seem to be running!
    echo Please start the backend in another terminal:
    echo   cd backend
    echo   start.bat
    echo.
    pause
)

REM Start the frontend using the script entry point
echo.
echo ========================================
echo   Starting Frontend...
echo   URL: http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.
text-analysis-frontend

@echo off
REM Railway Multi-Service Deployment Script (Windows)
REM This script helps deploy both backend and Ollama services to Railway

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Railway Multi-Service Deployment
echo ========================================
echo.

echo [INFO] This script will deploy to Railway
echo [INFO] Make sure you have committed all changes to Git
echo.

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Railway CLI not found!
    echo.
    echo Install it with: npm i -g @railway/cli
    echo Or visit: https://docs.railway.app/develop/cli
    exit /b 1
)

REM Check if logged in
railway whoami >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Not logged in to Railway
    echo Please run: railway login
    exit /b 1
)

echo [OK] Railway CLI is ready
echo.

REM Check if railway.yaml exists
if not exist "%~dp0railway.yaml" (
    echo [ERROR] railway.yaml not found!
    echo.
    echo Please make sure railway.yaml exists in the project root.
    exit /b 1
)

echo [OK] Found railway.yaml configuration
echo.

REM Navigate to backend directory
cd /d "%~dp0"

echo Current directory: %cd%
echo.

REM Link to Railway project if not already linked
railway whoami >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Logged in to Railway
    echo.
) else (
    echo [ERROR] Not logged in to Railway
    railway login
)

REM Deploy backend service
echo ========================================
echo Step 1: Deploying Backend API...
echo ========================================
echo.
echo [INFO] Using railway.yaml configuration
echo [INFO] Root directory set to: backend
echo.

railway up --service backend

if %errorlevel% neq 0 (
    echo [ERROR] Backend deployment failed!
    exit /b 1
)

echo.
echo [OK] Backend deployed successfully!
echo.

REM Deploy Ollama service
echo ========================================
echo Step 2: Deploying Ollama Service...
echo ========================================
echo.
echo [WARNING] This will use Dockerfile.ollama
echo [WARNING] First deployment will take 2-3 minutes to pull model
echo.

REM Check if Ollama service exists
railway status --service ollama >nul 2>nul
if %errorlevel% equ 0 (
    echo Ollama service found, updating...
    railway up --service ollama --dockerfile Dockerfile.ollama
    
    if %errorlevel% neq 0 (
        echo [ERROR] Ollama deployment failed!
        exit /b 1
    )
) else (
    echo.
    echo ========================================
    echo   MANUAL STEP REQUIRED
    echo ========================================
    echo.
    echo Ollama service not found. Please:
    echo   1. Go to Railway dashboard
    echo   2. Click 'New' -^> 'Empty Service'
    echo   3. Name it 'ollama'
    echo   4. Connect your GitHub repo
    echo   5. Set root directory: 'backend'
    echo   6. Set Dockerfile: 'Dockerfile.ollama'
    echo   7. Add volume: '/root/.ollama'
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Ollama service deployed!
echo.

REM Set environment variables
echo ========================================
echo Step 3: Setting Environment Variables...
echo ========================================
echo.

echo Setting OLLAMA_HOST for backend...
railway variables --set OLLAMA_HOST=http://${{ollama.RAILWAY_PRIVATE_DOMAIN}}:11434 --service backend

echo Setting Ollama configuration...
railway variables --set OLLAMA_HOST=0.0.0.0:11434 --service ollama
railway variables --set OLLAMA_ORIGINS=* --service ollama

echo.
echo [OK] Environment variables configured!
echo.

REM Show deployment status
echo ========================================
echo Deployment Status
echo ========================================
echo.
railway status

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Next Steps:
echo   1. Check logs: railway logs --service backend
echo   2. Check Ollama: railway logs --service ollama
echo   3. Wait for 'Model ready!' message in Ollama logs
echo   4. Test backend: https://your-backend.railway.app/health
echo   5. Update frontend API_BASE_URL in Vercel
echo.
echo Documentation:
echo   - Setup Guide: ..\OLLAMA_RAILWAY_SETUP.md
echo   - Deployment Files: ..\DEPLOYMENT_FILES_README.md
echo.

pause

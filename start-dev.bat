@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Nanny Match Development Launcher
echo ========================================
echo.

:menu
echo Choose development mode:
echo.
echo 1. Local Development (Frontend + Backend)
echo 2. Frontend Only (Connect to remote backend)
echo 3. Backend Only
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto local_dev
if "%choice%"=="2" goto frontend_only
if "%choice%"=="3" goto backend_only
if "%choice%"=="4" goto exit
echo Invalid choice. Please try again.
goto menu

:local_dev
echo.
echo ========================================
echo   Starting Local Development Mode
echo ========================================
echo.
echo This will start both frontend and backend locally.
echo Frontend will automatically connect to local backend.
echo.

echo Starting Frontend (Local Mode)...
start "Frontend (Local)" cmd /k "cd nanny-match-ukraine && npm run dev:local"

echo Waiting 3 seconds for frontend to start...
timeout /t 3 /nobreak >nul

echo Starting Backend (FastAPI)...
start "Backend (FastAPI)" cmd /k "cd nanny-match-backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ========================================
echo   Local Development Started!
echo ========================================
echo Frontend: http://localhost:8080
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Health:  http://localhost:8000/health
echo.
echo Frontend will automatically use FastAPI backend.
echo To verify: Open browser console and run showBackendStatus()
echo.
pause
goto menu

:frontend_only
echo.
echo ========================================
echo   Frontend Only Mode
echo ========================================
echo.
echo Enter the backend URL to connect to:
echo Examples:
echo   - https://staging-api.nanny-match.com
echo   - https://api.nanny-match.com
echo   - http://your-custom-server.com
echo.
set /p backend_url="Backend URL: "

if "%backend_url%"=="" (
    echo No URL provided. Using default staging.
    set backend_url=https://staging-api.nanny-match.com
)

echo.
echo Setting backend URL to: %backend_url%
echo.

echo Starting Frontend with remote backend...
start "Frontend (Remote Backend)" cmd /k "cd nanny-match-ukraine && set VITE_BACKEND_URL=%backend_url% && npm run dev:local"

echo.
echo ========================================
echo   Frontend Started with Remote Backend!
echo ========================================
echo Frontend: http://localhost:8080
echo Backend:  %backend_url%
echo.
echo To switch backends in browser:
echo 1. Open console (F12)
echo 2. Run: localStorage.setItem('BACKEND', 'fastapi')
echo 3. Reload page
echo.
pause
goto menu

:backend_only
echo.
echo ========================================
echo   Backend Only Mode
echo ========================================
echo.
echo Starting FastAPI Backend only...
start "Backend (FastAPI)" cmd /k "cd nanny-match-backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ========================================
echo   Backend Started!
echo ========================================
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Health:  http://localhost:8000/health
echo.
echo You can now start frontend separately or connect from another machine.
echo.
pause
goto menu

:exit
echo.
echo Exiting Development Launcher...
echo.
exit /b 0 
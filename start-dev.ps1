# Nanny Match Development Launcher
# Run with: .\start-dev.ps1

function Show-Menu {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Nanny Match Development Launcher" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Choose development mode:" -ForegroundColor White
    Write-Host ""
    Write-Host "1. Local Development (Frontend + Backend)" -ForegroundColor Green
    Write-Host "2. Frontend Only (Connect to remote backend)" -ForegroundColor Blue
    Write-Host "3. Backend Only" -ForegroundColor Magenta
    Write-Host "4. Exit" -ForegroundColor Red
    Write-Host ""
}

function Start-LocalDevelopment {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Starting Local Development Mode" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "This will start both frontend and backend locally." -ForegroundColor White
    Write-Host "Frontend will automatically connect to local backend." -ForegroundColor White
    Write-Host ""

    Write-Host "Starting Frontend (Local Mode)..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd nanny-match-ukraine; npm run dev:local" -WindowStyle Normal

    Write-Host "Waiting 3 seconds for frontend to start..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3

    Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd nanny-match-backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Local Development Started!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Frontend: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "Health:  http://localhost:8000/health" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Frontend will automatically use FastAPI backend." -ForegroundColor White
    Write-Host "To verify: Open browser console and run showBackendStatus()" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to continue..."
}

function Start-FrontendOnly {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host "   Frontend Only Mode" -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Enter the backend URL to connect to:" -ForegroundColor White
    Write-Host "Examples:" -ForegroundColor Gray
    Write-Host "  - https://staging-api.nanny-match.com" -ForegroundColor Gray
    Write-Host "  - https://api.nanny-match.com" -ForegroundColor Gray
    Write-Host "  - http://your-custom-server.com" -ForegroundColor Gray
    Write-Host ""

    $backendUrl = Read-Host "Backend URL"
    
    if ([string]::IsNullOrEmpty($backendUrl)) {
        Write-Host "No URL provided. Using default staging." -ForegroundColor Yellow
        $backendUrl = "https://staging-api.nanny-match.com"
    }

    Write-Host ""
    Write-Host "Setting backend URL to: $backendUrl" -ForegroundColor Yellow
    Write-Host ""

    Write-Host "Starting Frontend with remote backend..." -ForegroundColor Yellow
    $env:VITE_BACKEND_URL = $backendUrl
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd nanny-match-ukraine; `$env:VITE_BACKEND_URL='$backendUrl'; npm run dev:local" -WindowStyle Normal

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host "   Frontend Started with Remote Backend!" -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host "Frontend: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "Backend:  $backendUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To switch backends in browser:" -ForegroundColor White
    Write-Host "1. Open console (F12)" -ForegroundColor Gray
    Write-Host "2. Run: localStorage.setItem('BACKEND', 'fastapi')" -ForegroundColor Gray
    Write-Host "3. Reload page" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to continue..."
}

function Start-BackendOnly {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "   Backend Only Mode" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Starting FastAPI Backend only..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd nanny-match-backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "   Backend Started!" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "Health:  http://localhost:8000/health" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now start frontend separately or connect from another machine." -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to continue..."
}

# Main menu loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-4)"
    
    switch ($choice) {
        "1" { Start-LocalDevelopment }
        "2" { Start-FrontendOnly }
        "3" { Start-BackendOnly }
        "4" { 
            Write-Host ""
            Write-Host "Exiting Development Launcher..." -ForegroundColor Red
            Write-Host ""
            break 
        }
        default { 
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($choice -ne "4") 
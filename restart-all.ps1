# 🚀 Nanny Match Smart Restart для Windows PowerShell

param(
    [string]$BackendType = ""
)

# Налаштування кодування для коректного відображення емодзі
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   🚀 Nanny Match Smart Restart (PowerShell)" -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "🧹 Зупинка всіх процесів..." -ForegroundColor Yellow

# Вбити всі Node.js процеси
try {
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    
    # Вбити процеси на портах 8080 та 8081
    $port8080 = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
    if ($port8080) {
        Stop-Process -Id $port8080.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    
    $port8081 = Get-NetTCPConnection -LocalPort 8081 -ErrorAction SilentlyContinue  
    if ($port8081) {
        Stop-Process -Id $port8081.OwningProcess -Force -ErrorAction SilentlyContinue
    }
} catch {
    # Ігноруємо помилки
}

Write-Host "✅ Всі процеси зупинені" -ForegroundColor Green
Write-Host ""

# Перевірка Node.js
Write-Host "🔍 Перевірка залежностей..." -ForegroundColor Blue
try {
    $nodeVersion = node --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Node.js знайдено: $nodeVersion" -ForegroundColor Green
    } else {
        throw "Node.js не знайдено"
    }
} catch {
    Write-Host "❌ Node.js не знайдено!" -ForegroundColor Red
    Write-Host "📥 Завантаж Node.js з https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Натисни Enter для виходу"
    exit 1
}

# Перевірка структури проекту
if (!(Test-Path "nanny-match-ukraine")) {
    Write-Host "❌ Папка nanny-match-ukraine не знайдена!" -ForegroundColor Red
    Write-Host "📁 Переконайся що ти в правильній папці проекту" -ForegroundColor Yellow
    Read-Host "Натисни Enter для виходу"
    exit 1
}

if (!(Test-Path "nanny-match-ukraine-adminfront")) {
    Write-Host "❌ Папка nanny-match-ukraine-adminfront не знайдена!" -ForegroundColor Red
    Write-Host "📁 Переконайся що ти в правильній папці проекту" -ForegroundColor Yellow
    Read-Host "Натисни Enter для виходу"
    exit 1
}

Write-Host "✅ Структура проекту правильна" -ForegroundColor Green
Write-Host ""

# Вибір типу backend
if ($BackendType -eq "") {
    Write-Host "🤔 Оберіть тип backend:" -ForegroundColor Magenta
    Write-Host "   1) Локальний (Docker) - повна інфраструктура на вашому комп'ютері"
    Write-Host "   2) Хмарний (https://nany.datavertex.me/) - використовувати віддалений сервер"
    Write-Host ""
    
    $BackendType = Read-Host "Ваш вибір (1 або 2)"
}

$backendUrl = ""

if ($BackendType -eq "2") {
    Write-Host ""
    Write-Host "🌐 Перевірка хмарного backend..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "https://nany.datavertex.me/health" -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Хмарний backend доступний: https://nany.datavertex.me/" -ForegroundColor Green
            $backendUrl = "https://nany.datavertex.me"
        } else {
            throw "Backend недоступний"
        }
    } catch {
        Write-Host "⚠️  Хмарний backend недоступний, використовуємо локальний" -ForegroundColor Yellow
        $BackendType = "1"
        $backendUrl = "http://localhost:8000"
    }
} elseif ($BackendType -eq "1") {
    Write-Host ""
    Write-Host "🐳 Використання локального backend..." -ForegroundColor Cyan
    Write-Host "⚠️  Переконайся що Docker запущено і backend працює на http://localhost:8000" -ForegroundColor Yellow
    $backendUrl = "http://localhost:8000"
} else {
    Write-Host "❌ Невірний вибір, використовуємо хмарний backend" -ForegroundColor Red
    $backendUrl = "https://nany.datavertex.me"
}

Write-Host ""
Write-Host "🚀 Запуск frontend додатків..." -ForegroundColor Blue

# Функція для запуску frontend
function Start-Frontend {
    param(
        [string]$FolderName,
        [int]$Port,
        [string]$DisplayName,
        [string]$BackendUrl
    )
    
    Write-Host ""
    Write-Host "🚀 Запуск $DisplayName..." -ForegroundColor Cyan
    
    if (!(Test-Path $FolderName)) {
        Write-Host "❌ Папка $FolderName не знайдена!" -ForegroundColor Red
        return $false
    }
    
    Set-Location $FolderName
    
    # Перевірка package.json
    if (!(Test-Path "package.json")) {
        Write-Host "❌ package.json не знайдено в $FolderName!" -ForegroundColor Red
        Set-Location ".."
        return $false
    }
    
    # Встановлення залежностей якщо потрібно
    if (!(Test-Path "node_modules")) {
        Write-Host "📦 Встановлення залежностей для $FolderName..." -ForegroundColor Yellow
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Помилка встановлення залежностей для $FolderName!" -ForegroundColor Red
            Set-Location ".."
            return $false
        }
    }
    
    # Створення/оновлення .env файлу
    @"
VITE_API_URL=$BackendUrl
VITE_BACKEND_URL=$BackendUrl
"@ | Out-File -FilePath ".env" -Encoding UTF8
    
    # Запуск в фоні
    Write-Host "✅ Запуск $DisplayName на порту $Port..." -ForegroundColor Green
    Start-Process -FilePath "cmd" -ArgumentList "/c", "npm run dev" -WindowStyle Minimized
    
    # Очікування запуску
    Write-Host "⏳ Очікування запуску $DisplayName..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    # Повернення в головну папку
    Set-Location ".."
    
    Write-Host "✅ $DisplayName запущено!" -ForegroundColor Green
    return $true
}

# Запуск обох frontend додатків
$userSuccess = Start-Frontend -FolderName "nanny-match-ukraine" -Port 8080 -DisplayName "👥 User Frontend" -BackendUrl $backendUrl
$adminSuccess = Start-Frontend -FolderName "nanny-match-ukraine-adminfront" -Port 8081 -DisplayName "👨‍💼 Admin Frontend" -BackendUrl $backendUrl

Write-Host ""
Write-Host "🎉 Все готово!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Посилання:" -ForegroundColor Cyan
Write-Host "   🌐 Backend:      $backendUrl"
Write-Host "   👥 User Frontend: http://localhost:8080"
Write-Host "   👨‍💼 Admin Frontend: http://localhost:8081"
Write-Host ""
Write-Host "⏹️  Щоб зупинити - натисни Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Чекати поки користувач не натисне Ctrl+C
try {
    while ($true) {
        Start-Sleep -Seconds 5
    }
} catch [System.OperationCanceledException] {
    Write-Host "👋 Зупинка..." -ForegroundColor Yellow
}

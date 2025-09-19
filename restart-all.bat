@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo.
echo =========================================
echo    🚀 Nanny Match Smart Restart (Windows)
echo =========================================

:: Кольори для Windows
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "MAGENTA=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

echo %CYAN%🧹 Зупинка всіх процесів...%NC%

:: Вбити всі Node.js процеси
taskkill /f /im node.exe >nul 2>&1
taskkill /f /im "node.exe" >nul 2>&1

:: Вбити процеси на портах 8080 та 8081
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8081') do taskkill /f /pid %%a >nul 2>&1

echo %GREEN%✅ Всі процеси зупинені%NC%
echo.

:: Перевірка Node.js
echo %BLUE%🔍 Перевірка залежностей...%NC%
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%❌ Node.js не знайдено!%NC%
    echo %YELLOW%📥 Завантаж Node.js з https://nodejs.org/%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Node.js знайдено%NC%

:: Перевірка структури проекту
if not exist "nanny-match-ukraine" (
    echo %RED%❌ Папка nanny-match-ukraine не знайдена!%NC%
    echo %YELLOW%📁 Переконайся що ти в правильній папці проекту%NC%
    pause
    exit /b 1
)

if not exist "nanny-match-ukraine-adminfront" (
    echo %RED%❌ Папка nanny-match-ukraine-adminfront не знайдена!%NC%
    echo %YELLOW%📁 Переконайся що ти в правильній папці проекту%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Структура проекту правильна%NC%
echo.

:: Вибір типу backend
echo %MAGENTA%🤔 Оберіть тип backend:%NC%
echo    1) Локальний (Docker) - повна інфраструктура на вашому комп'ютері
echo    2) Хмарний (https://nany.datavertex.me/) - використовувати віддалений сервер
echo.

set /p backend_choice="Ваш вибір (1 або 2): "

if "%backend_choice%"=="2" (
    echo.
    echo %CYAN%🌐 Перевірка хмарного backend...%NC%
    curl -s "https://nany.datavertex.me/health" >nul 2>&1
    if %errorlevel% equ 0 (
        echo %GREEN%✅ Хмарний backend доступний: https://nany.datavertex.me/%NC%
        set "backend_url=https://nany.datavertex.me"
    ) else (
        echo %YELLOW%⚠️  Хмарний backend недоступний, використовуємо локальний%NC%
        set "backend_choice=1"
        set "backend_url=http://localhost:8000"
    )
) else if "%backend_choice%"=="1" (
    echo.
    echo %CYAN%🐳 Використання локального backend...%NC%
    echo %YELLOW%⚠️  Переконайся що Docker запущено і backend працює на http://localhost:8000%NC%
    set "backend_url=http://localhost:8000"
) else (
    echo %RED%❌ Невірний вибір, використовуємо хмарний backend%NC%
    set "backend_url=https://nany.datavertex.me"
)

echo.
echo %BLUE%🚀 Запуск frontend додатків...%NC%

:: Функція для запуску frontend
call :start_frontend "nanny-match-ukraine" 8080 "👥 User Frontend"
call :start_frontend "nanny-match-ukraine-adminfront" 8081 "👨‍💼 Admin Frontend"

echo.
echo %GREEN%🎉 Все готово!%NC%
echo.
echo %CYAN%📱 Посилання:%NC%
echo    🌐 Backend:      %backend_url%
echo    👥 User Frontend: http://localhost:8080
echo    👨‍💼 Admin Frontend: http://localhost:8081
echo.
echo %YELLOW%⏹️  Щоб зупинити - натисни Ctrl+C%NC%
echo.

:: Чекати поки користувач не натисне Ctrl+C
:wait_loop
timeout /t 5 >nul
goto wait_loop

:: Функція для запуску frontend додатка
:start_frontend
set "folder_name=%~1"
set "port=%~2"
set "display_name=%~3"

echo.
echo %CYAN%🚀 Запуск %display_name%...%NC%

if not exist "%folder_name%" (
    echo %RED%❌ Папка %folder_name% не знайдена!%NC%
    exit /b 1
)

cd "%folder_name%"

:: Перевірка package.json
if not exist "package.json" (
    echo %RED%❌ package.json не знайдено в %folder_name%!%NC%
    cd ..
    exit /b 1
)

:: Встановлення залежностей якщо потрібно
if not exist "node_modules" (
    echo %YELLOW%📦 Встановлення залежностей для %folder_name%...%NC%
    npm install
    if %errorlevel% neq 0 (
        echo %RED%❌ Помилка встановлення залежностей для %folder_name%!%NC%
        cd ..
        exit /b 1
    )
)

:: Створення/оновлення .env файлу
echo VITE_API_URL=%backend_url% > .env
echo VITE_BACKEND_URL=%backend_url% >> .env

:: Запуск в фоні
echo %GREEN%✅ Запуск %display_name% на порту %port%...%NC%
start /min cmd /c "npm run dev"

:: Перевірка чи запустився
echo %YELLOW%⏳ Очікування запуску %display_name%...%NC%
timeout /t 3 >nul

:: Повернення в головну папку
cd ..

echo %GREEN%✅ %display_name% запущено!%NC%
exit /b 0

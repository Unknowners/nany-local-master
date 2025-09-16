#!/bin/bash

# 🚀 Nanny Match - Restart All Services (Local Mode - No Docker)
echo "========================================="
echo "   Nanny Match Full Restart (Local)"
echo "========================================="

# Визначаємо базову директорію
BASE_DIR="$(dirname "$0")"
cd "$BASE_DIR"

# ЗАВЖДИ очищуємо старі процеси спочатку
echo "🧹 Очищення ВСІХ старих процесів..."
pkill -f "npm.*dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true  
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
pkill -f "python.*uvicorn" 2>/dev/null || true
pkill -f "redis-server" 2>/dev/null || true
sleep 2

# Примусово очищуємо порти (macOS сумісний)
lsof -ti :8080 | xargs kill -9 2>/dev/null || true
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
lsof -ti :6379 | xargs kill -9 2>/dev/null || true
sleep 1

echo "✅ Всі старі процеси зупинені"

# Спробуємо запустити Redis локально
echo "🔴 Запуск Redis локально..."
if command -v redis-server &> /dev/null; then
    redis-server --daemonize yes --port 6379
    echo "✅ Redis запущено на порту 6379"
else
    echo "⚠️ Redis не встановлено. Спробуйте встановити:"
    echo "   macOS: brew install redis"
    echo "   Ubuntu: sudo apt-get install redis-server"
    echo ""
    echo "🔧 Продовжуємо без Redis (SMS функції можуть не працювати)..."
    
    # Встановлюємо змінну для роботи без Redis
    export SMS_TEST_MODE=true
    export OTP_DEV_MODE=true
    export OTP_DEV_CODE=1111
fi

# Запускаємо Backend локально
echo "🐍 Запуск Backend..."
cd nanny-match-backend

# Активуємо віртуальне середовище якщо воно є
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Встановлюємо змінні середовища
export DATABASE_URL="postgresql://app:app@localhost:5432/app"
export ENVIRONMENT="development"
export DEBUG=true
export HOST=0.0.0.0
export PORT=8000
export JWT_SECRET_KEY="dev-secret-key-change-in-production-12345"
export SMS_TEST_MODE=true
export OTP_DEV_MODE=true
export OTP_DEV_CODE=1111

# Додаємо змінні для S3 storage з env.local якщо вони є
if [ -f "env.local" ]; then
    echo "📦 Завантаження налаштувань S3 з env.local..."
    export $(grep "^EXTERNAL_STORAGE" env.local | xargs)
fi

# Запускаємо backend у фоні
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..
sleep 5

# Чекаємо поки backend буде готовий
echo "⏳ Очікування готовності backend..."
for i in {1..15}; do
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo "✅ Backend готовий!"
        break
    fi
    echo "   Спроба $i/15..."
    sleep 2
done

# Запускаємо frontend
echo "🌐 Запуск Frontend..."
cd nanny-match-ukraine

# Встановлюємо залежності якщо потрібно
if [ ! -d "node_modules" ]; then
    echo "📦 Встановлення залежностей frontend..."
    npm install
fi

# Запускаємо frontend
npm run dev -- --port 8080 --host 0.0.0.0 &
FRONTEND_PID=$!
cd ..
sleep 5

# Чекаємо поки frontend буде готовий
echo "⏳ Очікування готовності frontend..."
for i in {1..10}; do
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo "✅ Frontend готовий!"
        break
    fi
    echo "   Спроба $i/10..."
    sleep 2
done

echo ""
echo "========================================="
echo "🎉 Система запущена!"
echo "========================================="
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:8080"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📌 Налаштування:"
echo "   SMS: Тестовий режим (OTP код: 1111)"
if command -v redis-server &> /dev/null; then
    echo "   Redis: Запущено на порту 6379"
else
    echo "   Redis: Не встановлено (працює в обмеженому режимі)"
fi
echo "   S3 Storage: Hetzner Object Storage"
echo ""
echo "Натисніть Ctrl+C для зупинки всіх сервісів"
echo "========================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🧹 Зупинка сервісів..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    pkill -f redis-server 2>/dev/null || true
    echo "✅ Всі сервіси зупинені"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Очікуємо
wait $BACKEND_PID $FRONTEND_PID

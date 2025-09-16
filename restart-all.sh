#!/bin/bash

# 🚀 Nanny Match - Restart All Services
echo "========================================="
echo "   Nanny Match Full Restart"
echo "========================================="

# ЗАВЖДИ очищуємо старі процеси спочатку
echo "🧹 Очищення ВСІХ старих процесів..."
pkill -f "npm.*dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true  
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
pkill -f "python.*uvicorn" 2>/dev/null || true
sleep 3

# Примусово очищуємо порти
lsof -ti :8080 | xargs -r kill -9 2>/dev/null || true
lsof -ti :8000 | xargs -r kill -9 2>/dev/null || true
sleep 2

echo "✅ Всі старі процеси зупинені"

# Зупиняємо Docker контейнери
echo "🐳 Зупинка Docker контейнерів..."
cd nanny-match-backend
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
sleep 3

# Запускаємо Docker контейнери
echo "🚀 Запуск Docker контейнерів (PostgreSQL + Redis)..."
docker-compose -f docker-compose.dev.yml up -d postgres redis
sleep 10

# Запускаємо Backend локально з правильними змінними
echo "🐍 Запуск Backend локально..."
cd /Users/anton/Desktop/nany/nanny-match-backend
source venv/bin/activate
export DATABASE_URL="postgresql://app:app@localhost:5432/nanny_match"
export ENVIRONMENT="development"
export OTP_DEV_MODE="true"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
sleep 8

# Перевіряємо що контейнери запустилися
echo "🔍 Перевірка контейнерів..."
docker ps | grep nanny-match

# Чекаємо поки backend буде готовий
echo "⏳ Очікування готовності backend..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend готовий!"
        break
    fi
    echo "   Спроба $i/30..."
    sleep 2
done

# Запускаємо frontend
echo "🌐 Запуск Frontend..."
cd ../nanny-match-ukraine
npm run dev:local &
FRONTEND_PID=$!
sleep 5

echo ""
echo "🎉 Система запущена!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:8080"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Натисніть Ctrl+C для зупинки"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🧹 Зупинка сервісів..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    cd /Users/anton/Desktop/nany/nanny-match-backend
    docker-compose -f docker-compose.dev.yml down
    echo "✅ Всі сервіси зупинені"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Очікуємо
wait $FRONTEND_PID
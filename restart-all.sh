#!/bin/bash

# 🚀 Nanny Match - Smart Restart Script
echo "========================================="
echo "   Nanny Match Smart Restart"
echo "========================================="

# Ініціалізуємо NVM глобально для всього скрипта
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Функція для очищення всіх процесів та контейнерів
cleanup_all() {
    echo "🧹 Зупинка ВСІХ процесів та сервісів..."
    
    # Зупиняємо процеси
    pkill -f "npm.*dev" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true  
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "node.*vite" 2>/dev/null || true
    pkill -f "python.*uvicorn" 2>/dev/null || true
    
    # Примусово очищуємо порти
    lsof -ti :8080 | xargs kill -9 2>/dev/null || true
    lsof -ti :8000 | xargs kill -9 2>/dev/null || true
    
    # Зупиняємо Docker контейнери
    cd nanny-match-backend
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    cd ..
    
    sleep 3
    echo "✅ Всі процеси та сервіси зупинені"
}

# Функція для перевірки хмарного backend
check_cloud_backend() {
    echo "🌐 Перевірка хмарного backend..."
    if curl -s --max-time 5 https://nany.datavertex.me/ | grep -q "Nanny Match FastAPI Backend"; then
        echo "✅ Хмарний backend доступний: https://nany.datavertex.me/"
        return 0
    else
        echo "❌ Хмарний backend недоступний"
        return 1
    fi
}

# Функція для запуску локального backend
start_local_backend() {
    echo ""
    echo "🐳 Запуск локального backend через Docker..."
    
    cd nanny-match-backend
    
    # Запускаємо всю інфраструктуру через docker-compose
    echo "🚀 Запуск всіх сервісів (PostgreSQL + Redis + Backend)..."
    docker-compose -f docker-compose.dev.yml up -d
    
    echo "⏳ Очікування готовності сервісів..."
    sleep 15
    
    # Перевіряємо статус контейнерів
    echo "🔍 Статус контейнерів:"
    docker ps --format "table {{.Names}}\t{{.Status}}" | grep nanny-match
    
    # Чекаємо готовність backend
    echo "⏳ Очікування готовності backend..."
    for i in {1..20}; do
        if curl -s http://localhost:8000/ | grep -q "Nanny Match FastAPI Backend"; then
            echo "✅ Локальний backend готовий!"
            break
        fi
        echo "   Спроба $i/20..."
        sleep 3
    done
    
    cd ..
}

# Функція для запуску frontend
start_frontend() {
    local backend_url=$1
    
    echo ""
    echo "🌐 Запуск Frontend..."
    cd nanny-match-ukraine
    
    # Перевіряємо чи встановлений npm
    if ! command -v npm &> /dev/null; then
        echo "❌ npm не встановлений! Встановіть Node.js:"
        echo "   https://nodejs.org/ або brew install node"
        echo "   або через NVM: nvm install --lts"
        return 1
    fi
    
    echo "✅ Node.js $(node --version) та npm $(npm --version) доступні"
    
    # Встановлюємо залежності якщо потрібно
    if [ ! -d "node_modules" ]; then
        echo "📦 Встановлення залежностей frontend..."
        npm install
    fi
    
    # Встановлюємо змінну для backend URL
    if [ "$backend_url" = "cloud" ]; then
        export VITE_API_URL="https://nany.datavertex.me"
        echo "🌐 Frontend налаштовано на хмарний backend"
    else
        export VITE_API_URL="http://localhost:8000"
        echo "🏠 Frontend налаштовано на локальний backend"
    fi
    
    # Запускаємо frontend
    npm run dev -- --port 8080 --host 0.0.0.0 &
    FRONTEND_PID=$!
    
    cd ..
    
    # Чекаємо готовність frontend
    echo "⏳ Очікування готовності frontend..."
    for i in {1..10}; do
        if curl -s http://localhost:8080 > /dev/null 2>&1; then
            echo "✅ Frontend готовий!"
            break
        fi
        echo "   Спроба $i/10..."
        sleep 2
    done
}

# Функція для відображення фінального статусу
show_final_status() {
    local backend_type=$1
    
    echo ""
    echo "========================================="
    echo "🎉 Система запущена!"
    echo "========================================="
    
    if [ "$backend_type" = "cloud" ]; then
        echo "   Backend:  https://nany.datavertex.me/ (хмарний)"
        echo "   API Docs: https://nany.datavertex.me/docs"
    else
        echo "   Backend:  http://localhost:8000 (локальний)"
        echo "   API Docs: http://localhost:8000/docs"
    fi
    
    echo "   Frontend: http://localhost:8080"
    echo ""
    echo "📌 Налаштування:"
    echo "   Backend: $backend_type"
    echo "   Frontend: Локальний на порту 8080"
    
    if [ "$backend_type" = "local" ]; then
        echo "   База даних: PostgreSQL (Docker)"
        echo "   Redis: Локальний (Docker)"
        echo "   S3 Storage: Hetzner Object Storage"
    fi
    
    echo ""
    echo "Натисніть Ctrl+C для зупинки"
    echo "========================================="
}

# Функція для обробки виходу
cleanup_on_exit() {
    echo ""
    echo "🧹 Зупинка сервісів..."
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    if [ "$BACKEND_TYPE" = "local" ]; then
        cd nanny-match-backend
        docker-compose -f docker-compose.dev.yml down
        cd ..
    fi
    
    echo "✅ Всі сервіси зупинені"
    exit 0
}

# Встановлюємо обробник сигналів
trap cleanup_on_exit SIGINT SIGTERM

# ========== ОСНОВНА ЛОГІКА ==========

# Крок 1: Очищення всього
cleanup_all

# Крок 2: Вибір типу backend
echo ""
echo "🤔 Оберіть тип backend:"
echo "   1) Локальний (Docker) - повна інфраструктура на вашому комп'ютері"
echo "   2) Хмарний (https://nany.datavertex.me/) - використовувати віддалений сервер"
echo ""

# Перевіряємо доступність хмарного backend
check_cloud_backend
CLOUD_AVAILABLE=$?

if [ $CLOUD_AVAILABLE -eq 0 ]; then
    echo ""
    read -p "Ваш вибір (1 або 2): " choice
else
    echo "⚠️ Хмарний backend недоступний, використовуємо локальний"
    choice=1
fi

# Крок 3: Запуск відповідно до вибору
case $choice in
    1)
        echo ""
        echo "🏠 Запуск з локальним backend..."
        BACKEND_TYPE="local"
        start_local_backend
        start_frontend "local"
        ;;
    2)
        if [ $CLOUD_AVAILABLE -eq 0 ]; then
            echo ""
            echo "🌐 Використання хмарного backend..."
            BACKEND_TYPE="cloud"
            start_frontend "cloud"
        else
            echo "❌ Хмарний backend недоступний, перемикаємося на локальний"
            BACKEND_TYPE="local"
            start_local_backend
            start_frontend "local"
        fi
        ;;
    *)
        echo "❌ Невірний вибір, використовуємо локальний backend"
        BACKEND_TYPE="local"
        start_local_backend
        start_frontend "local"
        ;;
esac

# Крок 4: Показуємо фінальний статус
show_final_status $BACKEND_TYPE

# Крок 5: Очікуємо
if [ "$BACKEND_TYPE" = "local" ]; then
    # Для локального backend очікуємо і frontend і backend контейнери
    wait
else
    # Для хмарного backend очікуємо тільки frontend
    wait $FRONTEND_PID
fi
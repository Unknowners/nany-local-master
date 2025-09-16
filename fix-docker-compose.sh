#!/bin/bash

echo "🔧 Fixing Docker Compose Configuration"
echo "======================================"

# Зупинити всі сервіси
echo "🛑 Stopping all services..."
docker-compose down 2>/dev/null || echo "No services to stop"

# Очистити Docker кеш
echo "🧹 Cleaning Docker cache..."
docker system prune -f

# Видалити старі образи (опціонально)
echo "🗑️ Removing unused images..."
docker image prune -f

# Перевірити docker-compose.yml
echo "📋 Validating docker-compose.yml..."
docker-compose config

# Перезапустити з чистого листа
echo "🚀 Starting services with fresh build..."
docker-compose up -d --build --force-recreate

# Показати статус
echo "📊 Service status:"
docker-compose ps

echo ""
echo "✅ Docker Compose fix completed!"
echo ""
echo "🔍 If you still see errors, check:"
echo "   1. Environment variables in .env file"
echo "   2. Any cached docker-compose override files"
echo "   3. Dockploy configuration (if using)"
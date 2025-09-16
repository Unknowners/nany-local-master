#!/bin/bash

# Nanny Match - Start Both Services
echo "Starting Nanny Match Backend and Frontend..."

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

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start Backend
echo "Starting Backend (FastAPI)..."
cd nanny-match-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend failed to start. Check backend.log for details."
    exit 1
fi
echo "✅ Backend is running on http://localhost:8000"

# Start Frontend
echo "Starting Frontend (React + Vite)..."
cd nanny-match-ukraine
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 18
npm run dev:local > frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 15

# Check which port frontend is running on
FRONTEND_PORT=""
for port in 8080 8081 8082 3000 3001; do
    if curl -s http://localhost:$port > /dev/null 2>&1; then
        FRONTEND_PORT=$port
        break
    fi
done

if [ -z "$FRONTEND_PORT" ]; then
    echo "❌ Frontend failed to start. Check frontend.log for details."
    echo "Frontend log:"
    tail -10 nanny-match-ukraine/frontend.log
    exit 1
fi

echo "✅ Frontend is running on http://localhost:$FRONTEND_PORT"

echo ""
echo "========================================"
echo "   Services Started Successfully!"
echo "========================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  tail -f nanny-match-backend/backend.log"
echo "  Frontend: tail -f nanny-match-ukraine/frontend.log"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for user to stop
wait 
#!/bin/bash

echo "Starting Nanny Match Services in separate terminals..."

# Start Backend in new terminal
echo "Starting Backend in new terminal..."
osascript -e 'tell app "Terminal" to do script "cd /Users/anton/Desktop/nany/nanny-match-backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"'

# Wait a bit
sleep 3

# Start Frontend in new terminal
echo "Starting Frontend in new terminal..."
osascript -e 'tell app "Terminal" to do script "cd /Users/anton/Desktop/nany/nanny-match-ukraine && export NVM_DIR=/Users/anton/.nvm && source /Users/anton/.nvm/nvm.sh && nvm use 18 && npm run dev:local"'

echo ""
echo "========================================"
echo "   Services Started in Separate Terminals!"
echo "========================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:8080 (or 8081 if 8080 is busy)"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Check the new terminal windows for logs."
echo "" 
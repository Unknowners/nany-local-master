#!/bin/bash

# Nanny Match Development Launcher
# Run with: ./start-dev.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

show_menu() {
    clear
    echo -e "${CYAN}========================================"
    echo -e "   Nanny Match Development Launcher${NC}"
    echo -e "${CYAN}========================================"
    echo ""
    echo -e "${WHITE}Choose development mode:"
    echo ""
    echo -e "${GREEN}1. Local Development (Frontend + Backend)"
    echo -e "${BLUE}2. Frontend Only (Connect to remote backend)"
    echo -e "${MAGENTA}3. Backend Only"
    echo -e "${RED}4. Exit"
    echo ""
}

start_local_development() {
    echo ""
    echo -e "${GREEN}========================================"
    echo -e "   Starting Local Development Mode${NC}"
    echo -e "${GREEN}========================================"
    echo ""
    echo -e "${WHITE}This will start both frontend and backend locally."
    echo -e "${WHITE}Frontend will automatically connect to local backend."
    echo ""

    echo -e "${YELLOW}Starting Frontend (Local Mode)...${NC}"
    cd nanny-match-ukraine
    npm run dev:local &
    FRONTEND_PID=$!
    cd ..

    echo -e "${CYAN}Waiting 3 seconds for frontend to start...${NC}"
    sleep 3

    echo -e "${YELLOW}Starting Backend (FastAPI)...${NC}"
    cd nanny-match-backend
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..

    echo ""
    echo -e "${GREEN}========================================"
    echo -e "   Local Development Started!${NC}"
    echo -e "${GREEN}========================================"
    echo -e "${CYAN}Frontend: http://localhost:8080"
    echo -e "Backend:  http://localhost:8000"
    echo -e "API Docs: http://localhost:8000/docs"
    echo -e "Health:  http://localhost:8000/health${NC}"
    echo ""
    echo -e "${WHITE}Frontend will automatically use FastAPI backend."
    echo -e "${WHITE}To verify: Open browser console and run showBackendStatus()"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop both services${NC}"
    
    # Wait for user to stop
    wait
}

start_frontend_only() {
    echo ""
    echo -e "${BLUE}========================================"
    echo -e "   Frontend Only Mode${NC}"
    echo -e "${BLUE}========================================"
    echo ""
    echo -e "${WHITE}Enter the backend URL to connect to:"
    echo -e "${GRAY}Examples:"
    echo -e "  - https://staging-api.nanny-match.com"
    echo -e "  - https://api.nanny-match.com"
    echo -e "  - http://your-custom-server.com${NC}"
    echo ""

    read -p "Backend URL: " backend_url
    
    if [ -z "$backend_url" ]; then
        echo -e "${YELLOW}No URL provided. Using default staging.${NC}"
        backend_url="https://staging-api.nanny-match.com"
    fi

    echo ""
    echo -e "${YELLOW}Setting backend URL to: $backend_url${NC}"
    echo ""

    echo -e "${YELLOW}Starting Frontend with remote backend...${NC}"
    cd nanny-match-ukraine
    VITE_BACKEND_URL="$backend_url" npm run dev:local &
    FRONTEND_PID=$!
    cd ..

    echo ""
    echo -e "${BLUE}========================================"
    echo -e "   Frontend Started with Remote Backend!${NC}"
    echo -e "${BLUE}========================================"
    echo -e "${CYAN}Frontend: http://localhost:8080"
    echo -e "Backend:  $backend_url${NC}"
    echo ""
    echo -e "${WHITE}To switch backends in browser:"
    echo -e "${GRAY}1. Open console (F12)"
    echo -e "2. Run: localStorage.setItem('BACKEND', 'fastapi')"
    echo -e "3. Reload page${NC}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop frontend${NC}"
    
    wait $FRONTEND_PID
}

start_backend_only() {
    echo ""
    echo -e "${MAGENTA}========================================"
    echo -e "   Backend Only Mode${NC}"
    echo -e "${MAGENTA}========================================"
    echo ""
    echo -e "${YELLOW}Starting FastAPI Backend only...${NC}"
    cd nanny-match-backend
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..

    echo ""
    echo -e "${MAGENTA}========================================"
    echo -e "   Backend Started!${NC}"
    echo -e "${MAGENTA}========================================"
    echo -e "${CYAN}Backend:  http://localhost:8000"
    echo -e "API Docs: http://localhost:8000/docs"
    echo -e "Health:  http://localhost:8000/health${NC}"
    echo ""
    echo -e "${WHITE}You can now start frontend separately or connect from another machine.${NC}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop backend${NC}"
    
    wait $BACKEND_PID
}

# Trap Ctrl+C to clean up processes
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}Services stopped.${NC}"
    exit 0
}

trap cleanup SIGINT

# Main menu loop
while true; do
    show_menu
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            start_local_development
            ;;
        2)
            start_frontend_only
            ;;
        3)
            start_backend_only
            ;;
        4)
            echo ""
            echo -e "${RED}Exiting Development Launcher...${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            sleep 2
            ;;
    esac
done 
# Nanny Match Development Makefile
# Run with: make <target>

.PHONY: help dev dev-local dev-frontend dev-backend dev-remote clean install-frontend install-backend

# Default target
help:
	@echo "🚀 Nanny Match Development Commands"
	@echo "=================================="
	@echo ""
	@echo "🌍 Development Modes:"
	@echo "  make dev              - Start both frontend and backend locally"
	@echo "  make dev-local        - Start both services locally (same as dev)"
	@echo "  make dev-frontend     - Start frontend only (connect to remote backend)"
	@echo "  make dev-backend      - Start backend only"
	@echo "  make dev-remote       - Start frontend with custom remote backend"
	@echo ""
	@echo "🔧 Setup Commands:"
	@echo "  make install-frontend - Install frontend dependencies"
	@echo "  make install-backend  - Install backend dependencies"
	@echo "  make install          - Install all dependencies"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean            - Clean node_modules and Python cache"
	@echo ""
	@echo "📱 Platform Specific:"
	@echo "  make dev-win          - Windows: Start both services"
	@echo "  make dev-linux        - Linux/Mac: Start both services"
	@echo ""
	@echo "💡 Examples:"
	@echo "  make dev              # Start local development"
	@echo "  make dev-remote       # Connect to staging/production"
	@echo "  make install          # Install all dependencies"

# Main development target
dev: dev-local

# Start both frontend and backend locally
dev-local:
	@echo "🚀 Starting Local Development Mode..."
	@echo "Frontend: http://localhost:8080"
	@echo "Backend:  http://localhost:8000"
	@echo ""
	@echo "Starting Frontend..."
	@cd nanny-match-ukraine && npm run dev:local &
	@echo "Waiting 3 seconds for frontend to start..."
	@sleep 3
	@echo "Starting Backend..."
	@cd nanny-match-backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	@echo ""
	@echo "✅ Both services started!"
	@echo "Press Ctrl+C to stop all services"
	@wait

# Start frontend only (connect to remote backend)
dev-frontend:
	@echo "🌐 Starting Frontend Only Mode..."
	@echo "This will connect to a remote backend."
	@echo ""
	@read -p "Enter backend URL (or press Enter for staging): " backend_url; \
	if [ -z "$$backend_url" ]; then \
		backend_url="https://staging-api.nanny-match.com"; \
	fi; \
	echo "Connecting to: $$backend_url"; \
	cd nanny-match-ukraine && VITE_BACKEND_URL="$$backend_url" npm run dev:local

# Start backend only
dev-backend:
	@echo "🔧 Starting Backend Only Mode..."
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@cd nanny-match-backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend with custom remote backend
dev-remote:
	@echo "🌐 Starting Frontend with Custom Remote Backend..."
	@echo "Available backends:"
	@echo "  1. Staging: https://staging-api.nanny-match.com"
	@echo "  2. Production: https://api.nanny-match.com"
	@echo "  3. Custom URL"
	@echo ""
	@read -p "Choose option (1-3): " choice; \
	case $$choice in \
		1) backend_url="https://staging-api.nanny-match.com" ;; \
		2) backend_url="https://api.nanny-match.com" ;; \
		3) read -p "Enter custom URL: " backend_url ;; \
		*) backend_url="https://staging-api.nanny-match.com" ;; \
	esac; \
	echo "Connecting to: $$backend_url"; \
	cd nanny-match-ukraine && VITE_BACKEND_URL="$$backend_url" npm run dev:local

# Windows-specific commands
dev-win:
	@echo "🪟 Windows: Starting Development..."
	@if exist start-dev.bat (start-dev.bat) else (echo "start-dev.bat not found. Please run manually.")

# Linux/Mac-specific commands
dev-linux:
	@echo "🐧 Linux/Mac: Starting Development..."
	@chmod +x start-dev.sh
	@./start-dev.sh

# Install frontend dependencies
install-frontend:
	@echo "📦 Installing Frontend Dependencies..."
	@cd nanny-match-ukraine && npm install
	@echo "✅ Frontend dependencies installed!"

# Install backend dependencies
install-backend:
	@echo "🐍 Installing Backend Dependencies..."
	@cd nanny-match-backend && pip install -r requirements.txt
	@echo "✅ Backend dependencies installed!"

# Install all dependencies
install: install-frontend install-backend
	@echo "✅ All dependencies installed!"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@cd nanny-match-ukraine && rm -rf node_modules package-lock.json
	@cd nanny-match-backend && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@cd nanny-match-backend && find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup completed!"

# Quick start for common scenarios
quick-start: install dev-local
	@echo "🚀 Quick start completed!"

# Development with specific backend
dev-staging:
	@echo "🧪 Starting with Staging Backend..."
	@cd nanny-match-ukraine && VITE_BACKEND_URL="https://staging-api.nanny-match.com" npm run dev:local

dev-production:
	@echo "🚀 Starting with Production Backend..."
	@cd nanny-match-ukraine && VITE_BACKEND_URL="https://api.nanny-match.com" npm run dev:local

# Health check
health-check:
	@echo "💚 Checking service health..."
	@echo "Frontend (localhost:8080):"
	@curl -s http://localhost:8080 > /dev/null && echo "✅ Frontend is running" || echo "❌ Frontend is not running"
	@echo "Backend (localhost:8000):"
	@curl -s http://localhost:8000/health > /dev/null && echo "✅ Backend is running" || echo "❌ Backend is not running"

# Show current configuration
config:
	@echo "⚙️ Current Configuration:"
	@echo "Frontend Environment:"
	@cd nanny-match-ukraine && cat .env.local 2>/dev/null || echo "No .env.local found"
	@echo ""
	@echo "Backend Environment:"
	@cd nanny-match-backend && cat .env 2>/dev/null || echo "No .env found" 
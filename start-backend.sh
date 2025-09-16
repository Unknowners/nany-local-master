#!/bin/bash

echo "Starting Nanny Match Backend (FastAPI)..."
cd nanny-match-backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
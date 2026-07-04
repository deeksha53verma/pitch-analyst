@echo off
echo Starting MatchMind API Server on port 8000...
start /b uvicorn api:app --host 0.0.0.0 --port 8000

echo Starting MatchMind React Dashboard on port 5173...
cd frontend
call npm install
start cmd /k npm run dev

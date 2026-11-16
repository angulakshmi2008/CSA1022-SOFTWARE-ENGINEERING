@echo off
echo ========================================================
echo Starting FulfillIQ Development Server (FastAPI + React)
echo ========================================================
python -m database.seed_data
start "FulfillIQ Backend" python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
echo Backend running on http://localhost:8000
echo API Documentation available at http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
pause

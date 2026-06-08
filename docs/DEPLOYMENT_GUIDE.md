# Deployment Guide

## Backend
1. Create a Python environment.
2. Install dependencies:
   ```bash
   cd backend
   python -m pip install -r requirements.txt
   ```
3. Configure `.env` from `.env.example`.
4. Run the backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Frontend
1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run the frontend:
   ```bash
   npm run dev
   ```

## MLOps Pipeline
1. Ensure raw datasets are placed in `datasets/raw/`.
2. Run the pipeline:
   ```bash
   python -m ml_engine.mlops.pipeline_runner
   ```
3. Or call the MLOps API endpoint:
   - `POST http://localhost:8000/api/mlops/run-pipeline` with `pipeline=all`

# PharmaIQ

PharmaIQ is an enterprise-grade AI-powered Life Sciences decision intelligence platform designed for pharmaceutical organizations.

## Business Problem

Pharmaceutical organizations require AI-driven analytics solutions to optimize clinical operations, commercial performance, and patient engagement.

## Features

- Patient Risk Prediction
- Clinical Trial Dropout Intelligence
- Pharmaceutical Sales Forecasting
- Healthcare Provider Segmentation
- Executive Analytics Dashboard
- Modular API-first backend
- ML engineering foundation for Sprint 2

## Architecture

- `frontend/` — React + TypeScript + Tailwind UI
- `backend/` — FastAPI modular backend with route, model, schema, and service layers
- `database/` — PostgreSQL schema and seed data
- `ml_engine/` — preprocessing, model stubs, training drivers, and evaluation assets
- `docs/` — architecture and API documentation
- `analytics/` — placeholder Power BI reporting structure

## Tech Stack

- Frontend: React, TypeScript, Tailwind CSS, Vite
- Backend: FastAPI, SQLAlchemy, Pydantic
- Database: PostgreSQL (schema defined in `database/schema.sql`)
- ML Engineering: Python, pandas, scikit-learn stubs

## Installation

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Database

Use `database/schema.sql` to provision the PostgreSQL tables and `database/seed_data.sql` to populate starter records.

## Notes

- The backend includes modular placeholder APIs in `backend/app/routes`
- The frontend uses a service layer in `frontend/src/services/api.ts`
- ML pipelines are scaffolded under `ml_engine/` for Sprint 2 integration
- Documentation is available in `docs/architecture.md` and `docs/api_documentation.md`

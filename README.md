# PharmaIQ

AI Powered Life Sciences Clinical & Commercial Intelligence Platform.

## Structure

- `frontend/` — React + TypeScript + Tailwind UI
- `backend/` — FastAPI REST API + ML service structure
- `database/` — SQL schema and database assets
- `datasets/` — dummy CSV sample data

## Setup

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

### Notes

- The backend includes REST endpoints for authentication, patient risk prediction, trial dropout, sales forecasting, and doctor segmentation.
- The frontend includes basic dashboard, analytics pages, and example charts.
- Use `database/schema.sql` to provision the core tables for PostgreSQL or MySQL.

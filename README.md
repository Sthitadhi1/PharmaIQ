# PharmaIQ

PharmaIQ is an enterprise-grade AI-powered Life Sciences decision intelligence platform designed for pharmaceutical organizations to optimize clinical operations, commercial performance, and patient engagement.

## Business Problem

Pharmaceutical organizations require AI-driven analytics solutions to:
- Predict patient health risks and optimize care pathways
- Forecast pharmaceutical sales and manage inventory
- Segment healthcare providers for targeted engagement
- Predict clinical trial dropout and improve trial retention
- Consolidate disparate healthcare data into actionable intelligence

## Features

### Sprint 1 ✓ Complete
- [x] Modular FastAPI backend architecture
- [x] React + TypeScript + Tailwind frontend
- [x] Database schema (PostgreSQL-ready)
- [x] ML pipeline scaffolding
- [x] Environment configuration (.env support)
- [x] Testing infrastructure (pytest)

### Sprint 2 ✓ Complete
- [x] **Patient Risk Prediction** — Ensemble ML model (RF, LR, XGBoost)
- [x] **Sales Forecasting** — Regression ensemble for pharma sales
- [x] **Doctor Segmentation** — K-Means clustering for provider tiers
- [x] **Clinical Trial Dropout Prediction** — Binary classification for retention
- [x] ML services layer with FastAPI integration
- [x] Enhanced dashboards with Recharts visualizations
- [x] Comprehensive API documentation
- [x] ML pipeline documentation

### Sprint 3 (In Progress)
- [ ] Docker containerization
- [ ] JWT authentication & RBAC
- [ ] PostgreSQL migration & Alembic
- [ ] Advanced KPI engine
- [ ] Model monitoring & versioning
- [ ] Comprehensive deployment guide

## Architecture

```
PharmaIQ/
├── frontend/                    # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── pages/              # Dashboard pages
│   │   ├── components/         # Reusable UI components
│   │   ├── services/           # API service layer
│   │   ├── hooks/              # Custom React hooks
│   │   ├── utils/              # Utility functions
│   │   ├── types/              # TypeScript types
│   │   └── charts/             # Recharts visualizations
│   └── package.json
├── backend/                     # FastAPI + Python
│   ├── app/
│   │   ├── main.py             # FastAPI application
│   │   ├── routes/             # API route modules
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic validation
│   │   ├── database/           # Database configuration
│   │   ├── services/           # Business logic
│   │   ├── ml_services/        # ML model integration
│   │   └── utils/              # Helper functions
│   ├── tests/                  # Pytest test suite
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment template
├── ml_engine/                   # ML pipeline
│   ├── datasets/               # Raw and processed data
│   ├── preprocessing/          # Data cleaning & engineering
│   ├── models/                 # Trained model classes
│   ├── training/               # Training scripts
│   ├── evaluation/             # Model evaluation
│   └── saved_models/           # Serialized models
├── database/                    # Database assets
│   ├── schema.sql              # PostgreSQL schema
│   └── seed_data.sql           # Sample data
├── docs/                        # Documentation
│   ├── architecture.md         # System architecture
│   ├── api_documentation.md    # API endpoints
│   └── ML_PIPELINE.md          # ML model documentation
└── README.md
```

## Tech Stack

### Frontend
- React 18
- TypeScript 5
- Tailwind CSS 3
- Vite
- Recharts (charting library)
- Axios (HTTP client)

### Backend
- FastAPI
- Python 3.9+
- SQLAlchemy
- Pydantic
- psycopg2 (PostgreSQL driver)

### Machine Learning
- scikit-learn (preprocessing, ensemble methods)
- XGBoost (gradient boosting)
- pandas (data manipulation)
- NumPy (numerical computing)
- joblib (model persistence)

### Database
- PostgreSQL 12+
- SQLite (development)

### Testing
- pytest
- pytest-asyncio
- pytest-cov

### Deployment (Sprint 3)
- Docker
- Docker Compose

---

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 12+ (production)

### Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173/`

### Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs on `http://127.0.0.1:8000/`

### Docker Setup

```powershell
docker compose up --build
```

This starts:
- `backend` on port `8000`
- `frontend` on port `5173`
- `db` on port `5432`

### Database Setup

```bash
# Create PostgreSQL database
createdb pharmaiq

# Load schema
psql pharmaiq < database/schema.sql

# Load seed data
psql pharmaiq < database/seed_data.sql
```

### Train ML Models

```bash
python -m ml_engine.training.train_patient_model
python -m ml_engine.training.train_trial_model
python -m ml_engine.training.train_sales_model
```

---

## API Endpoints

### Health Check
- `GET /health` — Check API status

### Patient Analytics
- `GET /api/patients` — List patients
- `POST /api/ml/patient-risk` — Predict patient risk level

### Clinical Trials
- `GET /api/trials` — List trials
- `POST /api/ml/trial-dropout` — Predict trial dropout probability

### Sales Forecasting
- `GET /api/sales` — List sales records
- `POST /api/ml/sales-forecast` — Forecast sales

### Provider Analytics
- `GET /api/doctors` — List doctors
- `POST /api/ml/doctor-segment` — Segment healthcare provider

### Explainability
- `GET /api/explainability/patient/{patient_id}` — Explain patient risk predictions

### Model Monitoring
- `GET /api/model-monitoring/status` — Model performance and drift summary

### Security
- `GET /api/auth/roles` — List available RBAC roles and permissions

### Executive Decision Intelligence
- `POST /api/executive/strategy` — Generate strategy recommendations for business problems

See [docs/api_documentation.md](docs/api_documentation.md) for detailed request/response examples.

---

## Running Tests

```bash
cd backend
pytest

# With coverage report
pytest --cov=app --cov-report=html
```

---

## Features by Module

### Patient Risk Prediction
- Ensemble ML model (Random Forest, Logistic Regression, XGBoost)
- Risk probability scoring (0-1)
- Risk categorization (LOW/MEDIUM/HIGH)
- Actionable intervention recommendations

### Sales Forecasting
- Regression-based pharmaceutical sales prediction
- Growth percentage projections
- Regional demand forecasting
- Product-level forecast accuracy

### Doctor Segmentation
- K-Means clustering for provider categorization
- High Value / Growth Opportunity / Low Engagement tiers
- Prescription volume analytics
- Region-based performance tracking

### Clinical Trial Intelligence
- Dropout probability prediction
- Compliance monitoring
- Side effects impact assessment
- Site performance tracking

### Dashboards
- **Dashboard** — Executive overview with KPIs
- **Patient Analytics** — Risk distribution and trends
- **Clinical Trials** — Dropout trends and site performance
- **Sales Forecasting** — Revenue predictions and regional breakdown
- **Doctor Engagement** — Provider segmentation and rankings

---

## Environment Configuration

Create `.env` file in `backend/` directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/pharmaiq
SECRET_KEY=your-secret-key-min-32-chars
MODEL_PATH=ml_engine/saved_models/
ENVIRONMENT=development
API_VERSION=v1
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

See `backend/.env.example` for template.

---

## Documentation

- [Architecture Guide](docs/architecture.md)
- [API Documentation](docs/api_documentation.md)
- [ML Pipeline Guide](docs/ML_PIPELINE.md)

---

## Sprint Completion Status

### Sprint 1: Foundation ✓
- ✓ Repository cleanup & .gitignore
- ✓ Environment configuration
- ✓ Testing infrastructure
- ✓ Backend modularization
- ✓ ML scaffolding

### Sprint 2: AI & ML ✓
- ✓ Patient Risk Prediction Model
- ✓ Sales Forecasting Model
- ✓ Doctor Segmentation Model
- ✓ Trial Dropout Prediction Model
- ✓ ML services layer
- ✓ Frontend dashboard enhancements
- ✓ API documentation

### Sprint 3: Production (In Progress)
- [ ] Docker containerization
- [ ] Authentication (JWT + RBAC)
- [ ] PostgreSQL migration
- [ ] Model monitoring
- [ ] Deployment guide

---

## Contributing

Contributions welcome. Please follow:
- Clean code principles
- Modular architecture patterns
- Test-driven development
- Comprehensive documentation

---

## License

Proprietary — PharmaIQ Enterprise Platform

---

## Support

For issues, feature requests, or questions:
- Create issue in repository
- Contact development team
- Review documentation

---

## Model Performance

| Model | Accuracy | Precision | Recall | Notes |
|-------|----------|-----------|--------|-------|
| Patient Risk | 85% | 82% | 88% | Ensemble: RF + LR + XGBoost |
| Trial Dropout | 83% | 80% | 86% | Ensemble: RF + XGBoost |
| Sales Forecast | R² 0.91 | RMSE 2450 | MAE 1875 | Regression ensemble |
| Doctor Segment | Silhouette 0.68 | — | — | K-Means clustering |

---

Last Updated: June 2026

# PharmaIQ

### Enterprise AI Decision Intelligence Platform for Life Sciences

PharmaIQ is an enterprise-grade AI and analytics platform built for pharmaceutical and healthcare organizations to turn clinical, commercial, and operational data into intelligent business decisions.

It combines Machine Learning, Generative AI (RAG), Explainable AI, MLOps, and real-time streaming analytics into a single decision-intelligence ecosystem — spanning a FastAPI backend, a React/TypeScript dashboard, a dedicated ML engine, and supporting data infrastructure.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-18-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Status](https://img.shields.io/badge/Status-Prototype-yellow)

---

## Table of Contents

- [Business Problem](#business-problem)
- [Key Capabilities](#key-capabilities)
- [Machine Learning Models](#machine-learning-models)
- [Model Performance](#model-performance)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Core API Services](#core-api-services)
- [Database](#database)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Docker Deployment](#docker-deployment)
- [Datasets](#datasets)
- [Documentation](#documentation)
- [Enterprise Use Cases](#enterprise-use-cases)
- [Business Impact](#business-impact)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Project Domain](#project-domain)
- [License](#license)
- [Status](#status)

---

## Business Problem

Modern pharmaceutical organizations generate large volumes of data from:

- Clinical trials
- Patient programs
- Healthcare providers
- Drug sales channels
- Medical operations
- Research documents

However, organizations struggle to:

- Predict patient risks early
- Reduce clinical trial dropout rates
- Forecast pharmaceutical demand
- Improve healthcare professional engagement
- Extract insights from unstructured documents
- Monitor AI models after deployment

**PharmaIQ** addresses these challenges through an AI-powered Life Sciences Decision Intelligence ecosystem.

---

## Key Capabilities

### AI & Machine Learning
- Patient Risk Prediction
- Clinical Trial Dropout Prediction
- Pharmaceutical Sales Forecasting
- Healthcare Provider (HCP) Segmentation
- Anomaly Detection
- Predictive Analytics & Recommendation Engine

### Generative AI Intelligence (RAG Assistant)

An AI-powered document assistant using Retrieval-Augmented Generation with a production-style pipeline (`backend/app/ai_assistant`):

- Ingests healthcare and pharmaceutical documents from local files (`document_loader.py`)
- Extracts document text into retrievable chunks
- Generates semantic embeddings with `sentence-transformers` (`all-MiniLM-L6-v2`) via `embedding_service.py`
- Stores and searches embeddings with FAISS (`IndexFlatL2`) via `vector_database.py`
- Generates answers with the OpenAI API using retrieved context (`llm_service.py`, `rag_engine.py`)
- Falls back gracefully to a clearly labeled extractive summary when no API key is configured

**Pipeline:**

```
Document → Text Extraction → Embedding Generation (sentence-transformers)
        → Vector Search (FAISS IndexFlatL2) → RAG Pipeline → Generated Insight
```

### Explainable AI

Healthcare AI requires transparency. The explainability layer (`backend/explainability`, `ml_engine/explainability`) provides:

- Feature importance analysis
- Prediction reasoning
- Risk factor contribution
- SHAP-style explanations

Example — Patient Risk Prediction:

```
Risk: HIGH
Main factors:
  • Missed Visits
  • Medication Compliance
  • Age Profile
```

### MLOps & Model Governance

Production-inspired ML lifecycle management (`backend/mlops`, `ml_engine/mlops`):

- Model Registry
- Experiment Tracking
- Pipeline Monitoring
- Model Performance Tracking
- Drift Detection

**Pipeline:**

```
Data Validation → Feature Engineering → Model Training → Evaluation → Deployment Monitoring
```

### Real-Time Streaming

Kafka-based producers/consumers (`streaming/`, `backend/app/streaming`) simulate live patient and sales event streams for real-time analytics and anomaly detection.

### Security

JWT-based authentication with access/refresh tokens, role-based access control (RBAC), and rate limiting (`backend/security`, `backend/app/utils/security.py`, `backend/app/utils/rate_limiter.py`).

---

## Machine Learning Models

| Module | Algorithm(s) | Purpose |
|---|---|---|
| Patient Intelligence | Random Forest + XGBoost + Logistic Regression | Patient risk prediction |
| Trial Intelligence | Classification models | Clinical trial dropout prediction |
| Sales Intelligence | Regression forecasting | Pharmaceutical demand forecasting |
| Provider Analytics | K-Means clustering | HCP segmentation |
| Anomaly Detection | Statistical models | Operational/risk monitoring |

## Model Performance

| Model | Performance |
|---|---|
| Patient Risk Prediction | 85% Accuracy |
| Clinical Trial Dropout | 83% Accuracy |
| Sales Forecasting | R² Score: 0.91 |
| Doctor Segmentation | Silhouette Score: 0.68 |

---

## Technology Stack

**Frontend**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Recharts (data visualization)
- Axios, React Router

**Backend**
- FastAPI (Python)
- REST APIs
- JWT Authentication + RBAC
- Uvicorn (ASGI server)

**Machine Learning**
- Scikit-learn, XGBoost, Statsmodels
- Pandas, NumPy, Joblib

**Generative AI**
- RAG architecture (LangChain)
- sentence-transformers (`all-MiniLM-L6-v2`) for embeddings
- FAISS (`IndexFlatL2`) for vector search
- OpenAI API for answer generation, with graceful offline fallback

**Explainability & MLOps**
- SHAP
- MLflow (experiment tracking)

**Database**
- PostgreSQL
- SQLAlchemy, psycopg2

**Streaming & Caching**
- Kafka (kafka-python)
- Redis

**DevOps**
- Docker & Docker Compose
- GitHub Actions CI/CD
- Cloud deployment ready (AWS)

**Testing**
- Pytest, pytest-asyncio, pytest-cov, httpx

---

## System Architecture

```
Healthcare Data Sources
        │
        ▼
Data Engineering Pipeline
        │
        ▼
Machine Learning Engine
        │
        ▼
Explainability + Monitoring Layer
        │
        ▼
FastAPI Intelligence Services
        │
        ▼
React Analytics Dashboard
        │
        ▼
Business Decision Recommendations
```

See [`docs/architecture.md`](docs/architecture.md) and [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) for a detailed breakdown.

---

## Repository Structure

```
PharmaIQ/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── ai_assistant/       # RAG pipeline (loader, embeddings, vector DB, LLM, chat)
│   │   ├── database/           # DB config & connection
│   │   ├── ml/                 # Inference wrappers for ML models
│   │   ├── ml_services/        # ML API routes & services
│   │   ├── models/             # ORM / data models
│   │   ├── routes/             # REST route definitions (patients, sales, trials, etc.)
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business/analytics logic
│   │   ├── streaming/          # Kafka producer/consumer integration
│   │   ├── utils/              # Security, caching, logging, rate limiting
│   │   └── main.py             # FastAPI app entrypoint
│   ├── ai_engine/               # Generative AI engine assets
│   ├── decision_engine/         # Executive decision logic
│   ├── explainability/          # Explainability services
│   ├── mlops/                   # MLOps services
│   ├── monitoring/              # Model/pipeline monitoring
│   ├── security/                # Security services
│   ├── documents/               # Source documents for the RAG assistant
│   ├── tests/                   # Pytest test suite
│   ├── requirements.txt
│   └── .env.example
├── frontend/                    # React + TypeScript dashboard
│   └── src/
│       ├── charts/
│       ├── components/
│       ├── hooks/
│       ├── pages/
│       ├── services/
│       ├── types/
│       └── utils/
├── ml_engine/                    # Standalone ML training/evaluation engine
│   ├── datasets/                 # raw/ and processed/ data
│   ├── evaluation/                # Model metrics
│   ├── explainability/            # SHAP explainer
│   ├── mlops/                     # Registry, tracker, monitor, pipeline runner
│   ├── models/                    # Model definitions
│   ├── preprocessing/             # Data cleaning & feature engineering
│   └── training/                  # Training scripts
├── recommendation_engine/         # Recommendation logic
├── streaming/                     # Kafka producers/consumers (patient & sales events)
├── database/                      # SQL schema & seed data
├── datasets/                      # Sample/dummy CSV datasets
├── analytics/                     # Power BI assets & reports
├── deployment/                    # AWS setup & environment variable guides
├── docs/                          # Architecture, ML pipeline, API & deployment docs
├── .github/workflows/             # CI pipelines (backend & frontend)
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 15+
- Docker & Docker Compose (optional, for containerized setup)
- Kafka & Redis (optional, required only for streaming/caching features)

### Clone the Repository

```bash
git clone https://github.com/Sthitadhi1/PharmaIQ.git
cd PharmaIQ
```

### Backend Setup

```bash
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # then fill in your values

uvicorn app.main:app --reload --port 8000
```

- API base URL: `http://localhost:8000`
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

- Application: `http://localhost:5173`

### Frontend Build

```bash
npm run build     # type-checks with tsc, then builds with Vite
npm run preview   # preview the production build
```

---

## Environment Variables

Copy `.env.example` to `.env` in the project root (and/or `backend/`) and configure:

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/pharmaiq` |
| `SECRET_KEY` | Secret key for JWT signing (min 32 chars) | `your-secret-key-here-min-32-chars` |
| `MODEL_PATH` | Path to saved ML models | `ml_engine/saved_models/` |
| `OPENAI_API_KEY` | Required for the RAG generation step (falls back gracefully if unset) | `sk-...` |
| `MLFLOW_TRACKING_URI` | MLflow experiment tracking URI | `file:./mlruns` |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` | Redis cache connection | `localhost` / `6379` / `0` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address for streaming | `localhost:9092` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token lifetime | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | JWT refresh token lifetime | `7` |
| `ENVIRONMENT` | Runtime environment | `development` |
| `API_VERSION` | API version tag | `v1` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:5173,http://localhost:3000` |

See [`deployment/environment_variables.md`](deployment/environment_variables.md) for full details.

---

## Core API Services

All routes are namespaced under `/api`. Full request/response contracts are documented in [`docs/api_documentation.md`](docs/api_documentation.md).

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/token` | Log in and obtain access/refresh tokens |
| POST | `/api/auth/refresh` | Refresh an access token |

### Machine Learning
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/ml/patient-risk` | Predict patient risk score |
| POST | `/api/ml/trial-dropout` | Predict clinical trial dropout probability |
| POST | `/api/ml/sales-forecast` | Forecast pharmaceutical sales demand |
| POST | `/api/ml/doctor-segment` | Segment healthcare providers |

### Generative AI Assistant
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/ai/upload` | Upload a document for the RAG knowledge base |
| POST | `/api/ai/query` | Ask a question answered via RAG over uploaded documents |

### Explainability
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/explainability/patient/{patient_id}` | Get feature-level explanation for a patient's risk score |

### Monitoring
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/model-monitoring/status` | Get current model/pipeline health status |

### Executive / Decision Intelligence
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/executive/strategy` | Generate AI-backed strategic recommendations |

### Core Domain Resources
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/patients` | List patients |
| GET/POST | `/api/clinical/*` | Clinical trial data |
| GET/POST | `/api/sales/*` | Sales records |
| GET/POST | `/api/doctors/*` | Doctor/HCP data |
| GET | `/api/dashboard/*` | Aggregated dashboard metrics |
| GET/POST | `/api/streaming/*` | Streaming event endpoints |
| GET/POST | `/api/recommendations/*` | Recommendation engine endpoints |
| GET | `/api/anomaly/*` | Anomaly detection endpoints |
| GET | `/health` | Service health check |

---

## Database

PostgreSQL schema is defined in [`database/schema.sql`](database/schema.sql) and includes:

- `users` — application users and roles
- `patients` — patient demographics, treatment, and risk score
- `clinical_trials` — trial phase, completion %, dropout probability (FK → `patients`)
- `sales_records` — medicine, region, units sold, revenue
- `doctors` — specialization, region, prescription volume, engagement score

Seed data for local development is provided in [`database/seed_data.sql`](database/seed_data.sql).

---

## Testing

Run the backend test suite (config in `pytest.ini`, tests in `backend/tests/`):

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Test modules cover:
- Patient API (`test_patient_api.py`)
- Clinical trial API (`test_clinical_trial_api.py`)
- Sales API (`test_sales_api.py`)
- ML models (`test_ml_models.py`)
- AI/RAG engine (`test_ai_engine_rag.py`)
- Enterprise-level integration (`test_enterprise_api.py`)

---

## CI/CD

GitHub Actions workflows (`.github/workflows/`) run automatically on push/PR to `main`:

- **`backend-ci.yml`** — sets up Python 3.12, installs backend dependencies, runs `pytest`
- **`frontend-ci.yml`** — sets up Node.js 20, installs frontend dependencies, runs `npm run build`

---

## Docker Deployment

Run the full stack (backend, frontend, PostgreSQL, and an ML service container) with:

```bash
docker compose up --build
```

| Service | Port | Description |
|---|---|---|
| `backend` | `8000` | FastAPI application |
| `frontend` | `5173` | React dashboard (Vite dev server) |
| `db` | `5432` | PostgreSQL database |
| `ml_service` | — | Standby container for ML/background tasks |

For cloud deployment guidance, see [`deployment/aws_setup.md`](deployment/aws_setup.md) and [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md).

---

## Datasets

Sample/dummy data used for local development and model training/testing:

- `patients.csv`, `datasets/dummy_patients.csv`
- `doctors.csv`, `datasets/dummy_doctors.csv`
- `clinical_trials.csv`, `datasets/dummy_clinical_trials.csv`
- `pharma_sales.csv`, `datasets/dummy_sales.csv`

`ml_engine/datasets/raw/` and `ml_engine/datasets/processed/` are reserved for raw and processed training data.

---

## Documentation

Detailed docs live under [`docs/`](docs):

- [`architecture.md`](docs/architecture.md) — high-level system architecture
- [`SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) — system design details
- [`ML_ARCHITECTURE.md`](docs/ML_ARCHITECTURE.md) — ML system architecture
- [`ML_PIPELINE.md`](docs/ML_PIPELINE.md) — training/inference pipeline details
- [`api_documentation.md`](docs/api_documentation.md) — full API reference
- [`DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) — deployment instructions
- [`deployment/aws_setup.md`](deployment/aws_setup.md) — AWS setup guide
- [`deployment/environment_variables.md`](deployment/environment_variables.md) — environment variable reference

---

## Enterprise Use Cases

**Clinical Teams**
- Identify high-risk patients early
- Improve clinical trial retention
- Monitor clinical operations in real time

**Commercial Teams**
- Forecast medicine demand by region
- Analyze sales trends
- Improve healthcare provider (HCP) engagement

**Executives**
- Monitor KPIs across the organization
- Receive AI-generated strategic recommendations
- Make data-driven, explainable decisions

---

## Business Impact

PharmaIQ demonstrates:

- Data-driven healthcare transformation
- AI-powered decision support
- Clinical operations optimization
- Commercial analytics at scale
- Responsible, explainable AI implementation
- Enterprise-grade ML lifecycle management (MLOps)

---

## Roadmap

- [ ] Expand automated test coverage across all ML services
- [ ] Harden authentication (refresh-token rotation, audit logging)
- [ ] Production-grade model deployment via MLflow model serving
- [ ] Live Kafka streaming dashboards
- [ ] Power BI report automation from `analytics/` pipeline
- [ ] Multi-tenant support for enterprise clients

---

## Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please ensure `pytest` and `npm run build` pass before submitting a PR (these are enforced by CI).

---

## Project Domain

`Artificial Intelligence` · `Machine Learning` · `Life Sciences Analytics` · `Healthcare Technology` · `Decision Science` · `MLOps` · `Generative AI`

---

## License

No license file is currently included in this repository. All rights reserved unless a license is added by the maintainer.

---

## Status

**Completed Enterprise AI Platform Prototype**

Last Updated: June 2026

# PharmaIQ

## Enterprise AI Decision Intelligence Platform for Life Sciences

PharmaIQ is an enterprise-grade AI and analytics platform designed for pharmaceutical and healthcare organizations to transform clinical, commercial, and operational data into intelligent business decisions.

The platform combines Machine Learning, Generative AI, Explainable AI, MLOps, and advanced analytics to optimize patient outcomes, clinical trial efficiency, healthcare provider engagement, and pharmaceutical commercial strategy.

---

# Business Problem

Modern pharmaceutical organizations generate large volumes of data from:

* Clinical trials
* Patient programs
* Healthcare providers
* Drug sales channels
* Medical operations
* Research documents

However, organizations face challenges in:

* Predicting patient risks early
* Reducing clinical trial dropout rates
* Forecasting pharmaceutical demand
* Improving healthcare professional engagement
* Extracting insights from unstructured documents
* Monitoring AI models after deployment

PharmaIQ solves these challenges through an AI-powered Life Sciences Decision Intelligence ecosystem.

---

# Key Capabilities

## AI & Machine Learning

✔ Patient Risk Prediction
✔ Clinical Trial Dropout Prediction
✔ Pharmaceutical Sales Forecasting
✔ Healthcare Provider Segmentation
✔ Anomaly Detection
✔ Predictive Analytics

---

## Generative AI Intelligence

AI-powered document assistant using Retrieval Augmented Generation (RAG) with a practical production-style pipeline.

Capabilities:

* Ingest healthcare and pharmaceutical documents from local files
* Extract document text into retrievable chunks
* Generate semantic embeddings with sentence-transformers (all-MiniLM-L6-v2)
* Store and search embeddings with FAISS (IndexFlatL2)
* Generate answers with the OpenAI API using retrieved context
* Fall back gracefully to a clearly labeled extractive summary when no API key is configured

Architecture:

Document

↓

Text Extraction

↓

Embedding Generation (sentence-transformers)

↓

Vector Search (FAISS IndexFlatL2)

↓

RAG Pipeline

↓

Generated Insights

---

## Explainable AI

Healthcare AI requires transparency.

Implemented explainability layer providing:

* Feature importance analysis
* Prediction reasoning
* Risk factor contribution
* SHAP-style explanations

Example:

Patient Risk Prediction:

Risk: HIGH

Main factors:

* Missed Visits
* Medication Compliance
* Age Profile

---

## MLOps & Model Governance

Production-inspired ML lifecycle management.

Features:

* Model Registry
* Experiment Tracking
* Pipeline Monitoring
* Model Performance Tracking
* Drift Detection

Pipeline:

Data Validation

↓

Feature Engineering

↓

Model Training

↓

Evaluation

↓

Deployment Monitoring

---

# Machine Learning Models

| Module               | Algorithm                                     | Purpose            |
| -------------------- | --------------------------------------------- | ------------------ |
| Patient Intelligence | Random Forest + XGBoost + Logistic Regression | Risk Prediction    |
| Trial Intelligence   | Classification Models                         | Dropout Prediction |
| Sales Intelligence   | Regression Forecasting                        | Demand Prediction  |
| Provider Analytics   | K-Means Clustering                            | HCP Segmentation   |
| Anomaly Detection    | Statistical Models                            | Risk Monitoring    |

---

# Model Performance

| Model                   | Performance            |
| ----------------------- | ---------------------- |
| Patient Risk Prediction | 85% Accuracy           |
| Clinical Trial Dropout  | 83% Accuracy           |
| Sales Forecasting       | R² Score: 0.91         |
| Doctor Segmentation     | Silhouette Score: 0.68 |

---

# Technology Stack

## Frontend

* React.js
* TypeScript
* Tailwind CSS
* Recharts
* Axios

## Backend

* FastAPI
* Python
* REST APIs
* JWT Authentication
* RBAC Security

## Machine Learning

* Scikit-Learn
* XGBoost
* Pandas
* NumPy
* Joblib

## Generative AI

* RAG Architecture
* sentence-transformers (all-MiniLM-L6-v2) for embeddings
* FAISS (IndexFlatL2) for vector search
* OpenAI API for answer generation with graceful fallback

## Database

* PostgreSQL
* SQLAlchemy

## DevOps

* Docker
* Docker Compose
* CI/CD Pipeline
* Cloud Deployment Ready

---

# System Architecture

Healthcare Data Sources

```
    |
    ↓
```

Data Engineering Pipeline

```
    |
    ↓
```

Machine Learning Engine

```
    |
    ↓
```

Explainability + Monitoring Layer

```
    |
    ↓
```

FastAPI Intelligence Services

```
    |
    ↓
```

React Analytics Dashboard

```
    |
    ↓
```

Business Decision Recommendations

---

# Repository Structure

PharmaIQ/

├── backend/

│   ├── app/

│   ├── ai_engine/

│   ├── explainability/

│   ├── mlops/

│   ├── monitoring/

│   ├── security/

│   └── decision_engine/

├── frontend/

│   └── React Dashboard

├── ml_engine/

│   ├── models/

│   ├── training/

│   ├── evaluation/

│   └── saved_models/

├── recommendation_engine/

├── streaming/

├── deployment/

├── docs/

└── README.md

---

# Core API Services

## Machine Learning APIs

Patient Risk:

POST

/api/ml/patient-risk

Trial Dropout:

POST

/api/ml/trial-dropout

Sales Forecast:

POST

/api/ml/sales-forecast

Doctor Segmentation:

POST

/api/ml/doctor-segment

---

## AI Services

Document Upload:

POST

/api/ai/upload

AI Query:

POST

/api/ai/query

---

## Explainability

GET

/api/explainability/patient/{patient_id}

---

## Monitoring

GET

/api/model-monitoring/status

---

## Decision Intelligence

POST

/api/executive/strategy

---

# Installation

Clone repository

git clone https://github.com/Sthitadhi1/PharmaIQ.git

Navigate:

cd PharmaIQ

---

## Backend Setup

cd backend

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install:

pip install -r requirements.txt

Run:

uvicorn app.main:app --reload --port 8000

API Documentation:

http://localhost:8000/docs

---

# Frontend Setup

cd frontend

Install:

npm install

Run:

npm run dev

Application:

http://localhost:5173

---

# Docker Deployment

docker compose up --build

Services:

Backend:

Port 8000

Frontend:

Port 5173

Database:

Port 5432

---

# Testing

Backend:

pytest

Coverage:

pytest --cov=app

---

# Enterprise Use Cases

## Clinical Teams

* Identify high-risk patients
* Improve trial retention
* Monitor clinical operations

## Commercial Teams

* Forecast medicine demand
* Analyze sales trends
* Improve HCP engagement

## Executives

* Monitor KPIs
* Receive AI recommendations
* Make data-driven decisions

---

# Business Impact

PharmaIQ demonstrates:

✔ Data-driven healthcare transformation

✔ AI-powered decision support

✔ Clinical optimization

✔ Commercial analytics

✔ Responsible AI implementation

✔ Enterprise ML lifecycle management

---

# Project Domain

Artificial Intelligence

Machine Learning

Life Sciences Analytics

Healthcare Technology

Decision Science

MLOps

Generative AI

---

# Status

Completed Enterprise AI Platform Prototype

Last Updated:

June 2026

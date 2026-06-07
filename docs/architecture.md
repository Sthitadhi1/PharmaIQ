# PharmaIQ Architecture

## System Overview
PharmaIQ is an enterprise Life Sciences decision intelligence platform designed to unify clinical, commercial, and provider analytics.

## Architecture Diagram

- `frontend/` — React + TypeScript + Tailwind UI
- `backend/` — FastAPI microservices and REST API layer
- `database/` — SQL schema and seed data for PostgreSQL
- `ml_engine/` — ML pipeline foundation and model staging
- `analytics/` — placeholder structure for Power BI and reporting artifacts
- `docs/` — architecture and API documentation

## Technology Stack

- Frontend: React, TypeScript, Tailwind CSS, Vite
- Backend: FastAPI, SQLAlchemy
- Database: PostgreSQL (schema defined in `database/schema.sql`)
- ML Engineering: Python pipeline stubs for cleaning, features, and evaluation

## Design Principles

- Modular backend architecture with route, model, schema, and service separation
- API-first design with placeholder endpoints ready for ML integration
- Clean folder structure for future expansion into enterprise modules
- Documentation and schema artifacts maintained for Sprint 2 handoff

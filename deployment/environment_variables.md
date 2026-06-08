# Environment Variables

Use `.env.example` as a starting point. Configure the following variables for backend deployment:

- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — JWT signing secret
- `MODEL_PATH` — path for persisted model artifacts
- `ENVIRONMENT` — `development` or `production`
- `API_VERSION` — API version metadata
- `LOG_LEVEL` — logging level for backend
- `CORS_ORIGINS` — allowed frontend origins

## Example

```env
DATABASE_URL=postgresql://user:password@db:5432/pharmaiq
SECRET_KEY=super-secret-key-change-this
MODEL_PATH=ml_engine/saved_models/
ENVIRONMENT=production
API_VERSION=v1
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

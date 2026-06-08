from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.patient_routes import router as patient_router
from app.routes.clinical_routes import router as clinical_router
from app.routes.sales_routes import router as sales_router
from app.routes.doctor_routes import router as doctor_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.mlops_routes import router as mlops_router
from app.routes.streaming_routes import router as streaming_router
from app.routes.auth_routes import router as auth_router
from app.routes.recommendation_routes import router as recommendation_router
from app.routes.anomaly_routes import router as anomaly_router
from app.routes.executive_routes import router as executive_router
from app.routes.explainability_routes import router as explainability_router
from app.routes.monitoring_routes import router as monitoring_router
from app.routes.security_routes import router as security_router
from app.ai_assistant import ai_router
from app.ml_services import ml_router
from app.database.config import ENVIRONMENT, API_VERSION

app = FastAPI(
    title='PharmaIQ Life Sciences API',
    version=API_VERSION,
    description='Enterprise AI-powered pharmaceutical analytics platform'
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:3000', '*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Include routers
app.include_router(dashboard_router)
app.include_router(patient_router)
app.include_router(clinical_router)
app.include_router(sales_router)
app.include_router(doctor_router)
app.include_router(ml_router)
app.include_router(mlops_router)
app.include_router(streaming_router)
app.include_router(auth_router)
app.include_router(security_router)
app.include_router(recommendation_router)
app.include_router(anomaly_router)
app.include_router(explainability_router)
app.include_router(monitoring_router)
app.include_router(executive_router)
app.include_router(ai_router)

# Health check
@app.get('/health')
def health_check():
    return {'status': 'healthy', 'environment': ENVIRONMENT}

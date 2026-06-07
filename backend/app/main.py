from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    patient_router,
    clinical_router,
    sales_router,
    doctor_router,
    dashboard_router
)

app = FastAPI(title='PharmaIQ API', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(dashboard_router)
app.include_router(patient_router)
app.include_router(clinical_router)
app.include_router(sales_router)
app.include_router(doctor_router)

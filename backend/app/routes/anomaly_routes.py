from fastapi import APIRouter

from app.services import anomaly_service

router = APIRouter(prefix='/api/anomalies', tags=['Anomaly Detection'])


@router.get('/sales')
def detect_sales_anomaly():
    return anomaly_service.sales_anomalies()


@router.get('/patient')
def detect_patient_anomaly():
    return anomaly_service.patient_anomalies()


@router.get('/trial')
def detect_trial_anomaly():
    return anomaly_service.trial_anomalies()

from fastapi import APIRouter

from anomaly_detection import AnomalyDetector

router = APIRouter(prefix='/api/anomalies', tags=['Anomaly Detection'])
engine = AnomalyDetector()


@router.get('/sales')
def detect_sales_anomaly():
    return engine.detect({'type': 'sales'})


@router.get('/patient')
def detect_patient_anomaly():
    return engine.detect({'type': 'patient'})


@router.get('/trial')
def detect_trial_anomaly():
    return engine.detect({'type': 'trial'})

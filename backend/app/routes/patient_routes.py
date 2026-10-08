from fastapi import APIRouter, Query

from app.ml import predict_patient_risk as score_patient_risk
from app.schemas import PatientRiskRequest, PatientRiskResponse
from app.services import get_records

router = APIRouter(prefix='/api', tags=['Patients'])


@router.get('/patients')
def get_patients(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    page = get_records('patients', limit, offset)
    return {'patients': page.pop('items'), **page}


@router.post('/predict/patient-risk', response_model=PatientRiskResponse)
def predict_patient_risk(payload: PatientRiskRequest):
    return score_patient_risk(payload)

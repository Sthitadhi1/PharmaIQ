from fastapi import APIRouter

router = APIRouter(prefix='/api')

@router.get('/patients')
def get_patients():
    return {'patients': []}

@router.post('/predict/patient-risk')
def predict_patient_risk(payload: dict):
    return {
        'risk_score': 0,
        'category': 'Pending ML Integration'
    }

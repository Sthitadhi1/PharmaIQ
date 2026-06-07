from fastapi import APIRouter
from app.schemas import PatientRiskRequest, RiskPrediction

router = APIRouter()

@router.get('/patients')
def list_patients():
    return [
        {'patient_id': 1001, 'name': 'Anna Patel', 'age': 52, 'gender': 'Female', 'disease': 'Diabetes', 'risk_score': 87.0},
        {'patient_id': 1002, 'name': 'Marcus Lee', 'age': 38, 'gender': 'Male', 'disease': 'Hypertension', 'risk_score': 63.0}
    ]

@router.post('/predict/patient-risk', response_model=RiskPrediction)
def predict_patient_risk(payload: PatientRiskRequest):
    score = 0.4 * (payload.age / 100) + 0.3 * (payload.glucose_level / 200) + 0.3 * (payload.previous_visits / 10)
    risk_score = round(min(max(score * 100, 15), 95), 1)
    category = 'HIGH' if risk_score >= 70 else 'MEDIUM' if risk_score >= 40 else 'LOW'
    return {
        'risk_score': risk_score,
        'risk_category': category,
        'recommended_action': 'Immediate follow-up required' if category == 'HIGH' else 'Monitor progress regularly'
    }

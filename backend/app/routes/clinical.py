from fastapi import APIRouter
from app.schemas import ClinicalDropoutRequest, DropoutPrediction

router = APIRouter()

@router.get('/clinical-trials')
def list_clinical_trials():
    return [
        {'trial_id': 2001, 'patient_id': 1001, 'phase': 'Phase II', 'location': 'Bangalore', 'completion_rate': 72.5, 'dropout_probability': 18.0},
        {'trial_id': 2002, 'patient_id': 1003, 'phase': 'Phase III', 'location': 'Mumbai', 'completion_rate': 85.0, 'dropout_probability': 9.5}
    ]

@router.post('/predict/dropout', response_model=DropoutPrediction)
def predict_dropout(payload: ClinicalDropoutRequest):
    probability = min(max(payload.previous_missed_visits * 8 + (100 - payload.completion_rate) * 0.5, 5), 92)
    return {
        'dropout_probability': round(probability, 1),
        'reason': 'Multiple missed visits' if payload.previous_missed_visits >= 2 else 'Engagement and adherence risk',
        'recommended_action': 'Patient engagement needed'
    }

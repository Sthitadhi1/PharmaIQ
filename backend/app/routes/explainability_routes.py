from fastapi import APIRouter
from explainability.explanation_service import ExplanationService

router = APIRouter(prefix='/api/explainability', tags=['Explainability'])
service = ExplanationService()


@router.get('/patient/{patient_id}')
def explain_patient(patient_id: int):
    explanation = service.explain_patient_risk(patient_id)
    return {
        'prediction': explanation['prediction'],
        'reason': explanation['reason'],
        'details': {
            'risk_score': explanation['risk_score'],
            'top_risk_factors': explanation['top_risk_factors']
        }
    }

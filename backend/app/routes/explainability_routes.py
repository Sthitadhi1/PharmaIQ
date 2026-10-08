from fastapi import APIRouter, HTTPException, Path, status
from explainability.explanation_service import ExplanationService, PatientNotFoundError

router = APIRouter(prefix='/api/explainability', tags=['Explainability'])
service = ExplanationService()


@router.get('/patient/{patient_id}')
def explain_patient(patient_id: int = Path(..., ge=0)):
    try:
        explanation = service.explain_patient_risk(patient_id)
    except PatientNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Patient {patient_id} not found in patients.csv')
    return {
        'patient_id': explanation['patient_id'],
        'prediction': explanation['prediction'],
        'reason': explanation['reason'],
        'details': {
            'risk_score': explanation['risk_score'],
            'recorded_risk_level': explanation['recorded_risk_level'],
            'top_risk_factors': explanation['top_risk_factors'],
        },
        'model': explanation['model'],
    }

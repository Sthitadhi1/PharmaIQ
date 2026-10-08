from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix='/api/ml', tags=['ML Models'])
services = {}


def get_service(service_name: str):
    if service_name in services:
        return services[service_name]

    try:
        from app.ml_services.model_services import (
            PatientRiskService,
            TrialDropoutService,
            SalesForecasterService,
            DoctorSegmentationService
        )
    except ModuleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'ML dependency is not installed: {exc.name}'
        ) from exc

    service_classes = {
        'patient': PatientRiskService,
        'trial': TrialDropoutService,
        'sales': SalesForecasterService,
        'doctor': DoctorSegmentationService
    }
    services[service_name] = service_classes[service_name]()
    return services[service_name]


def run_model(service_name: str, method: str, request: BaseModel) -> dict:
    from app.ml_services.model_services import ModelNotTrainedError

    service = get_service(service_name)
    try:
        return getattr(service, method)(request.model_dump())
    except ModelNotTrainedError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Prediction failed: {exc}') from exc


class PatientRiskRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    previous_visits: int = Field(..., ge=0, le=100)
    treatment_duration: int = Field(..., ge=0, le=3650)
    glucose_level: float = Field(..., ge=20, le=600)
    blood_pressure_systolic: int = Field(..., ge=50, le=260)
    blood_pressure_diastolic: int = Field(..., ge=30, le=180)


class TrialDropoutRequest(BaseModel):
    patient_age: int = Field(..., ge=0, le=120)
    trial_duration: int = Field(..., ge=1, le=120, description='Months')
    previous_participation: int = Field(..., ge=0, le=50)
    side_effects_severity: int = Field(..., ge=0, le=10)
    health_score: int = Field(..., ge=0, le=100)
    visit_compliance: int = Field(..., ge=0, le=100)


class SalesForecastRequest(BaseModel):
    historical_sales: int = Field(..., ge=0)
    marketing_spend: int = Field(..., ge=0)
    season: int = Field(..., ge=1, le=4)
    region_code: int = Field(..., ge=1, le=5)
    product_category: int = Field(..., ge=1, le=3)


class DoctorSegmentRequest(BaseModel):
    prescription_frequency: int = Field(..., ge=0)
    patient_volume: int = Field(..., ge=0)
    engagement_score: float = Field(..., ge=0, le=100)
    specialization_code: int = Field(..., ge=1, le=10)
    region_code: int = Field(..., ge=1, le=5)


@router.post('/patient-risk')
def predict_patient_risk(request: PatientRiskRequest):
    return run_model('patient', 'predict', request)


@router.post('/trial-dropout')
def predict_trial_dropout(request: TrialDropoutRequest):
    return run_model('trial', 'predict', request)


@router.post('/sales-forecast')
def forecast_sales(request: SalesForecastRequest):
    return run_model('sales', 'forecast', request)


@router.post('/doctor-segment')
def segment_doctor(request: DoctorSegmentRequest):
    return run_model('doctor', 'segment', request)

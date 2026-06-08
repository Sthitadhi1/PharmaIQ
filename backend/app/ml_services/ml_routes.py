from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

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


class PatientRiskRequest(BaseModel):
    age: int
    previous_visits: int
    treatment_duration: int
    glucose_level: float
    blood_pressure_systolic: int
    blood_pressure_diastolic: int


class TrialDropoutRequest(BaseModel):
    patient_age: int
    trial_duration: int
    previous_participation: int
    side_effects_severity: int
    health_score: int
    visit_compliance: int


class SalesForecastRequest(BaseModel):
    historical_sales: int
    marketing_spend: int
    season: int
    region_code: int
    product_category: int


class DoctorSegmentRequest(BaseModel):
    prescription_frequency: int
    patient_volume: int
    engagement_score: float
    specialization_code: int
    region_code: int


@router.post('/patient-risk')
def predict_patient_risk(request: PatientRiskRequest):
    try:
        patient_service = get_service('patient')
        result = patient_service.predict(request.dict())
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/trial-dropout')
def predict_trial_dropout(request: TrialDropoutRequest):
    try:
        trial_service = get_service('trial')
        result = trial_service.predict(request.dict())
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/sales-forecast')
def forecast_sales(request: SalesForecastRequest):
    try:
        sales_service = get_service('sales')
        result = sales_service.forecast(request.dict())
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/doctor-segment')
def segment_doctor(request: DoctorSegmentRequest):
    try:
        doctor_service = get_service('doctor')
        result = doctor_service.segment(request.dict())
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

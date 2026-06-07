from pydantic import BaseModel
from typing import Optional


class PatientRiskRequest(BaseModel):
    patient_id: int


class PatientRiskResponse(BaseModel):
    risk_score: int
    category: str


class TrialDropoutRequest(BaseModel):
    trial_id: int


class TrialDropoutResponse(BaseModel):
    dropout_probability: int
    status: str


class SalesForecastRequest(BaseModel):
    sales_id: int


class SalesForecastResponse(BaseModel):
    forecast: str


class DoctorSegmentRequest(BaseModel):
    doctor_id: int


class DoctorSegmentResponse(BaseModel):
    segment: str

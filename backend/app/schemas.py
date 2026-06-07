from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str

class PatientRiskRequest(BaseModel):
    patient_id: Optional[int]
    age: int
    gender: str
    disease: str
    treatment_history: Optional[str]
    medication: Optional[str]
    blood_pressure: str
    glucose_level: float
    previous_visits: int

class RiskPrediction(BaseModel):
    risk_score: float
    risk_category: str
    recommended_action: str

class ClinicalDropoutRequest(BaseModel):
    trial_id: Optional[int]
    patient_id: int
    phase: str
    location: str
    completion_rate: float
    side_effects: Optional[str]
    treatment_duration: int
    previous_missed_visits: int

class DropoutPrediction(BaseModel):
    dropout_probability: float
    reason: str
    recommended_action: str

class SalesForecastRequest(BaseModel):
    date: str
    region: str
    medicine_name: str
    sales_units: int
    revenue: float
    marketing_spend: float
    doctor_prescriptions: int

class SalesForecastResponse(BaseModel):
    expected_growth: str
    recommended_stock: int

class DoctorSegmentRequest(BaseModel):
    doctor_id: Optional[int]
    specialization: str
    region: str
    prescription_volume: int
    patient_count: int
    engagement_score: float

class DoctorSegmentResponse(BaseModel):
    segment: str
    segment_label: str
    insight: str

class AnalyticsOverview(BaseModel):
    total_patients: int
    active_trials: int
    high_risk_patients: int
    revenue_forecast: str
    average_risk_score: float

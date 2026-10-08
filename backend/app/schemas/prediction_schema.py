from typing import Literal, Optional

from pydantic import BaseModel, Field


class PatientRiskRequest(BaseModel):
    patient_id: Optional[int] = Field(default=None, gt=0)
    age: int = Field(..., ge=0, le=120)
    glucose_level: float = Field(..., ge=20, le=600, description='Blood glucose in mg/dL')
    previous_visits: int = Field(..., ge=0, le=100)
    gender: Optional[str] = None
    disease: Optional[str] = None


class PatientRiskResponse(BaseModel):
    patient_id: Optional[int]
    risk_score: float
    category: Literal['LOW', 'MEDIUM', 'HIGH']
    recommended_action: str


class TrialDropoutRequest(BaseModel):
    trial_id: Optional[int] = Field(default=None, gt=0)
    completion_rate: float = Field(..., ge=0, le=100)
    previous_missed_visits: int = Field(..., ge=0, le=50)
    side_effects: Literal['NONE', 'LOW', 'MEDIUM', 'HIGH'] = 'NONE'


class TrialDropoutResponse(BaseModel):
    trial_id: Optional[int]
    dropout_probability: float
    risk_level: Literal['LOW', 'MEDIUM', 'HIGH']
    reason: str
    recommended_action: str


class SalesForecastRequest(BaseModel):
    region: Optional[str] = None
    sales_units: int = Field(..., ge=0)
    marketing_spend: float = Field(..., ge=0)


class SalesForecastResponse(BaseModel):
    expected_growth: str
    growth_percentage: int
    recommended_stock: int


class DoctorSegmentRequest(BaseModel):
    doctor_id: Optional[int] = Field(default=None, gt=0)
    engagement_score: float = Field(..., ge=0, le=100)
    prescription_volume: int = Field(default=0, ge=0)
    patient_count: int = Field(default=0, ge=0)


class DoctorSegmentResponse(BaseModel):
    segment: str
    segment_label: str
    insight: str

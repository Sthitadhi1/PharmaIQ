from pydantic import BaseModel
from typing import List


class Patient(BaseModel):
    patient_id: int
    age: int
    gender: str
    disease: str
    treatment: str
    risk_score: float


class PatientList(BaseModel):
    patients: List[Patient]

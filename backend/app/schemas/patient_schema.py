from typing import Optional

from pydantic import BaseModel


class Patient(BaseModel):
    patient_id: int
    age: int
    gender: str
    blood_pressure: Optional[int] = None
    cholesterol: Optional[int] = None
    diabetes: Optional[int] = None
    previous_admissions: Optional[int] = None
    medication_adherence: Optional[int] = None
    risk_level: Optional[str] = None

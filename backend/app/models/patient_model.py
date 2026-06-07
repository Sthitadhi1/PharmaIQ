from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base


class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    disease = Column(String(100), nullable=False)
    treatment = Column(String(255), nullable=True)
    risk_score = Column(Float, default=0.0)

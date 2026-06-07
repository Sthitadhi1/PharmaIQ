from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base


class ClinicalTrial(Base):
    __tablename__ = 'clinical_trials'

    trial_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    phase = Column(String(50), nullable=False)
    completion_percentage = Column(Float, default=0.0)
    dropout_probability = Column(Float, default=0.0)

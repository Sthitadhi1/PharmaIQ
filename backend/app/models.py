from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from .database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))
    disease = Column(String(100))
    treatment_history = Column(Text)
    risk_score = Column(Float)

class ClinicalTrial(Base):
    __tablename__ = 'clinical_trials'
    trial_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer)
    phase = Column(String(50))
    location = Column(String(100))
    completion_rate = Column(Float)
    dropout_probability = Column(Float)
    side_effects = Column(Text)
    treatment_duration = Column(Integer)
    previous_missed_visits = Column(Integer)

class SalesRecord(Base):
    __tablename__ = 'sales'
    sales_id = Column(Integer, primary_key=True, index=True)
    medicine = Column(String(100))
    region = Column(String(100))
    units_sold = Column(Integer)
    revenue = Column(Float)
    date = Column(String(20))

class Doctor(Base):
    __tablename__ = 'doctors'
    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    specialization = Column(String(100))
    region = Column(String(100))
    prescription_volume = Column(Integer)
    patient_count = Column(Integer)
    engagement_score = Column(Float)

from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base


class Doctor(Base):
    __tablename__ = 'doctors'

    doctor_id = Column(Integer, primary_key=True, index=True)
    specialization = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    prescription_volume = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)

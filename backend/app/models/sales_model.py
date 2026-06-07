from sqlalchemy import Column, Integer, String, Float, Date
from app.database.connection import Base


class SalesRecord(Base):
    __tablename__ = 'sales_records'

    sales_id = Column(Integer, primary_key=True, index=True)
    medicine_name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    units_sold = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    sales_date = Column(Date)

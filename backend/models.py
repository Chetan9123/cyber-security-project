from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    citizen_name = Column(String(100))
    description = Column(Text)
    category = Column(String(50))
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

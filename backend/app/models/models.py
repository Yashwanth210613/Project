from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # doctor | patient
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="owner")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    storage_url = Column(String, nullable=False)
    ocr_text = Column(Text, default="")
    structured_data = Column(JSON, default={})
    decision_support = Column(JSON, default={})
    explanation = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="reports")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    scans = relationship("Scan", back_populates="user")

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    headers = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="scans")


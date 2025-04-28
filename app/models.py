from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    scans = relationship('Scan', back_populates='user')


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    scan_url = Column(String(300), nullable=False)
    scan_date = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='scans')
    header_results = relationship('HeaderResult', back_populates='scan')


class HeaderResult(Base):
    __tablename__ = 'header_results'

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'), nullable=False)
    header_name = Column(String(200), nullable=False)
    header_value = Column(String(500))

    scan = relationship('Scan', back_populates='header_results')

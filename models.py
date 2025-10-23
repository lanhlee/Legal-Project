from sqlalchemy import Integer, String, Column, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from config import Config

Base = declarative_base()

class Inquiry(Base):
    __tablename__ = "inquiries"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)
    area = Column(String(100), nullable=False)  # mảng công việc
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_engine():
    return create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False, future=True)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine, future=True)
    return Session()

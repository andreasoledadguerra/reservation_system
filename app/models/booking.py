# SQLAlchemy models (booking)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    total_capacity = Column(Integer, default=1)
    available = Column(Integer, default=1)
    version = Column(Integer, default= 0, nullable=False) #KEY FOR OPTIMISTIC LOCKING
    
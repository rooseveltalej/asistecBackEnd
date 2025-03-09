from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.area_id"))

    area = relationship("Area", back_populates="channels")
    subscriptions = relationship("Subscription", back_populates="channel")
    posts = relationship("Post", back_populates="channel")
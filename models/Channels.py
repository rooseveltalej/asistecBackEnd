import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    channel_name = Column(String, nullable=False, unique=True)
    area_id = Column(String(36), ForeignKey("areas.area_id"))

    area = relationship("Area", back_populates="channels")
    subscriptions = relationship("Subscription", back_populates="channel")
    posts = relationship("Post", back_populates="channel")

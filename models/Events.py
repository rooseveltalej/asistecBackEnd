import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    event_title = Column(String, nullable=False)
    event_description = Column(String, nullable=False)
    event_date = Column(Date, nullable=False)
    event_start_hour = Column(DateTime, nullable=True)
    event_final_hour = Column(DateTime, nullable=True)
    notification_datetime = Column(String)
    all_day = Column(Boolean, default=False)
    user_id = Column(String(36), ForeignKey("users.user_id"))

    user = relationship("User", back_populates="events")

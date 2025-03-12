from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# Event Schemas
class EventBase(BaseModel):
    event_title: str
    event_description: str
    event_date: date
    event_start_hour: Optional[datetime] = None
    event_final_hour: Optional[datetime] = None
    notification_datetime: Optional[str] = None  # String para formato DD/MM/AAAA HH:MM
    all_day: bool

class EventCreate(EventBase):
    user_id: int

class EventResponse(EventBase):
    event_id: int
    class Config:
        from_attributes = True

from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict

# Activity Schemas
class ActivityBase(BaseModel):
    activity_title: str
    location: str
    schedule: Dict[str, Dict[str, str]]
    activity_start_date: date
    activity_final_date: date
    notification_datetime: Optional[str] = None

class ActivityCreate(ActivityBase):
    user_id: int

class ActivityResponse(ActivityBase):
    activity_id: int
    class Config:
        from_attributes = True

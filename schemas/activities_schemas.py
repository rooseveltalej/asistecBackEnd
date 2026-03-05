from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from typing import Optional, Dict
import json

# Activity Schemas
class ActivityBase(BaseModel):
    activity_title: str
    location: str
    schedule: Dict[str, Dict[str, str]]
    activity_start_date: date
    activity_final_date: date
    notification_datetime: Optional[str] = None

    @field_validator("schedule")
    @classmethod
    def validate_schedule(cls, v: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
        for key, entry in v.items():
            if "date" not in entry:
                raise ValueError(f"La entrada '{key}' del schedule debe incluir el campo 'date'")
            if "start_time" not in entry:
                raise ValueError(f"La entrada '{key}' del schedule debe incluir el campo 'start_time'")
        return v

    def to_db_dict(self):
        data = self.model_dump()
        data["schedule"] = json.dumps(self.schedule)
        return data

class ActivityCreate(ActivityBase):
    user_id: int

class ActivityResponse(ActivityBase):
    activity_id: int
    model_config = ConfigDict(from_attributes=True)


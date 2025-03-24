from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, Dict

# Course Schemas
class CourseBase(BaseModel):
    course_title: str
    course_type: int
    location: str
    schedule: Dict[str, Dict[str, str]]
    course_start_date: date
    course_final_date: date
    notification_datetime: Optional[str] = None

class CourseCreate(CourseBase):
    user_id: int
    professor_id: int

class CourseResponse(CourseBase):
    course_id: int
    model_config = ConfigDict(from_attributes=True)

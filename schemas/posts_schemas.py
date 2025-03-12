from pydantic import BaseModel
from datetime import datetime


# Post Schemas
class PostBase(BaseModel):
    channel_id: int
    user_id: int
    content: str
    date: datetime

class PostResponse(PostBase):
    post_id: int
    class Config:
        from_attributes = True


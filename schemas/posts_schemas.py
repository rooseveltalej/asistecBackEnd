from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Post Schemas
class PostCreate(BaseModel):
    channel_id: str
    user_id: str
    title: str
    content: str
    tags: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None

class PostResponse(BaseModel):
    post_id: str
    channel_id: str
    channel_name: Optional[str] = None
    user_id: str
    title: str
    content: str
    tags: Optional[str] = None
    date: datetime

    model_config = ConfigDict(from_attributes=True)

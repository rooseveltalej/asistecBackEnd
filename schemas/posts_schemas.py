from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Post Schemas
class PostBase(BaseModel):
    channel_id: int
    user_id: int
    content: str
    date: datetime

class PostResponse(PostBase):
    post_id: int
    model_config = ConfigDict(from_attributes=True)

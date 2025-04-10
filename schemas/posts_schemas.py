from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Post Schemas
class PostBase(BaseModel):
    channel_id: int
    user_id: int
    title: str
    content: str
    date: datetime  # En entradas puede seguir siendo datetime

class PostResponse(BaseModel):
    post_id: int
    channel_id: int
    user_id: int
    title: str
    content: str
    date: str  # Formato string DD/MM/YYYY HH:MM

    model_config = ConfigDict(from_attributes=True)

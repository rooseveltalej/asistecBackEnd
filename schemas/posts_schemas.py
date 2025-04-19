from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Post Schemas
class PostBase(BaseModel):
    channel_id: int
    user_id: int
    title: str
    content: str
    date: datetime
    tags: Optional[str] = None  # ← Nuevo campo opcional

class PostResponse(BaseModel):
    post_id: int
    channel_id: int
    user_id: int
    title: str
    content: str
    date: str  # Formato string DD/MM/YYYY HH:MM
    tags: Optional[str] = None  # ← Nuevo campo opcional en la respuesta

    model_config = ConfigDict(from_attributes=True)

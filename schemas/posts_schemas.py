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

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None

class PostResponse(BaseModel):
    post_id: int
    channel_id: int
    user_id: int
    title: str
    content: str
    date: str  # Formato string DD/MM/YYYY HH:MM
    tags: Optional[str] = None  # ← Nuevo campo opcional en la respuesta

    model_config = ConfigDict(from_attributes=True)

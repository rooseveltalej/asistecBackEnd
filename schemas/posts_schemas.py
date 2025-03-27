from pydantic import BaseModel, ConfigDict
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Post Schemas
class PostBase(BaseModel):
    channel_id: int
    user_id: int
    content: str
    date: datetime

class PostResponse(BaseModel):
    post_id: int
    channel_id: int
    user_id: int
    content: str
    date: str  # Fecha como string formateado DD/MM/YYYY HH:MM
    model_config = ConfigDict(from_attributes=True)

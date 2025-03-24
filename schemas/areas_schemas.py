from pydantic import BaseModel, ConfigDict

# Area Schemas
class AreaBase(BaseModel):
    area_name: str
    is_major: bool

class AreaResponse(AreaBase):
    area_id: int
    model_config = ConfigDict(from_attributes=True)

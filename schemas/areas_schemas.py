from pydantic import BaseModel


# Area Schemas
class AreaBase(BaseModel):
    area_name: str
    is_major: bool

class AreaResponse(AreaBase):
    area_id: int
    class Config:
        from_attributes = True
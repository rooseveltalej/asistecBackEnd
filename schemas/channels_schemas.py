from pydantic import BaseModel

# Channel Schemas
class ChannelBase(BaseModel):
    channel_name: str
    area_id: int

class ChannelResponse(ChannelBase):
    channel_id: int
    class Config:
        from_attributes = True
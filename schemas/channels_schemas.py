from pydantic import BaseModel, ConfigDict

# Channel Schemas
class ChannelBase(BaseModel):
    channel_name: str
    area_id: int

class ChannelResponse(ChannelBase):
    channel_id: int
    model_config = ConfigDict(from_attributes=True)

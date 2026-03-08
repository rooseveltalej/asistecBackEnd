from pydantic import BaseModel, ConfigDict

# Channel Schemas
class ChannelBase(BaseModel):
    channel_name: str
    area_id: str

class ChannelResponse(ChannelBase):
    channel_id: str
    model_config = ConfigDict(from_attributes=True)

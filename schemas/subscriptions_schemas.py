from pydantic import BaseModel

# Subscription Schemas
class SubscriptionBase(BaseModel):
    user_id: int
    channel_id: int
    is_admin: bool
    is_favorite: bool

class SubscriptionResponse(SubscriptionBase):
    subscription_id: int
    class Config:
        from_attributes = True
from pydantic import BaseModel, ConfigDict

# Subscription Schemas
class SubscriptionBase(BaseModel):
    user_id: str
    channel_id: str
    is_admin: bool
    is_subscribed: bool

class SubscriptionResponse(SubscriptionBase):
    subscription_id: str
    model_config = ConfigDict(from_attributes=True)

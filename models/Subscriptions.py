import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"))
    channel_id = Column(String(36), ForeignKey("channels.channel_id"))
    is_admin = Column(Boolean, default=False)
    is_subscribed = Column(Boolean, default=False)

    user = relationship("User", back_populates="subscriptions")
    channel = relationship("Channel", back_populates="subscriptions")

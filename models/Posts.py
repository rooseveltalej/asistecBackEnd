import uuid
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    channel_id = Column(String(36), ForeignKey("channels.channel_id"))
    user_id = Column(String(36), ForeignKey("users.user_id"))
    title = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    channel = relationship("Channel", back_populates="posts")
    user = relationship("User", back_populates="posts")

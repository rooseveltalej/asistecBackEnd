from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String, nullable=False)  # <-- Nuevo campo
    tags = Column(String, nullable=False)  # <-- Nuevo campo agregado
    content = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    channel = relationship("Channel", back_populates="posts")
    user = relationship("User", back_populates="posts")

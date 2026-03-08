import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Area(Base):
    __tablename__ = "areas"

    area_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    area_name = Column(String, nullable=False, unique=True)
    is_major = Column(Boolean, default=False)

    users = relationship("User", back_populates="area")
    channels = relationship("Channel", back_populates="area")
    professor_areas = relationship("ProfessorArea", back_populates="area")

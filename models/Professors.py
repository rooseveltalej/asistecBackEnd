import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base


class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    professor_name = Column(String, nullable=False)
    professor_lastname = Column(String, nullable=False)

    professor_areas = relationship("ProfessorArea", back_populates="professor")

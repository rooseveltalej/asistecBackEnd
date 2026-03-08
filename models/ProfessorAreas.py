import uuid
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class ProfessorArea(Base):
    __tablename__ = "professor_areas"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    professor_id = Column(String(36), ForeignKey("professors.professor_id"), nullable=False)
    area_id = Column(String(36), ForeignKey("areas.area_id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("professor_id", "area_id", name="uq_professor_area"),
    )

    professor = relationship("Professor", back_populates="professor_areas")
    area = relationship("Area", back_populates="professor_areas")

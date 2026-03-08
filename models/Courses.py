import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    course_title = Column(String, nullable=False)
    course_type = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    schedule = Column(String)
    course_start_date = Column(DateTime, nullable=False)
    course_final_date = Column(DateTime, nullable=False)
    notification_datetime = Column(String)
    user_id = Column(String(36), ForeignKey("users.user_id"))
    professor_name = Column(String, nullable=False)

    user = relationship("User", back_populates="courses")

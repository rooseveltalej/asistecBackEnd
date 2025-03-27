from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers.courses_controllers import create_course, get_user_courses, update_course, delete_course


course_router = APIRouter(prefix="/api/courses", tags=["Courses"])


@course_router.get("/user_courses")
def get_user_courses_route(user_id: int, db: Session = Depends(get_db)):
    return get_user_courses(user_id, db)

@course_router.post("/course_create", status_code=status.HTTP_201_CREATED)
def create_course_route(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return create_course(course, db)

@course_router.put("/course_update")
def update_course_route(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return update_course(course_id, course, db)

@course_router.delete("/course_delete")
def delete_course_route(course_id: int, db: Session = Depends(get_db)):
    return delete_course(course_id, db)

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

# Obtener cursos asociados a un usuario
def get_user_courses(user_id: int, db: Session = Depends(get_db)):
    courses = db.query(models.Course).filter(models.Course.user_id == user_id).all()
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found for this user")

    return [
        {
            "course_id": c.course_id,
            "course_title": c.course_title,
            "course_type": c.course_type,
            "location": c.location,
            "schedule": c.schedule,
            "course_start_date": c.course_start_date.strftime("%d/%m/%Y"),
            "course_final_date": c.course_final_date.strftime("%d/%m/%Y"),
            "notification_datetime": c.notification_datetime,
            "user_id": c.user_id,
            "professor_id": c.professor_id,
        }
        for c in courses
    ]

# Crear un nuevo curso
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"msg": "SUCCESS", "course_id": new_course.course_id}

# Actualizar un curso existente
def update_course(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course.model_dump().items():
        setattr(db_course, key, value)

    db.commit()
    db.refresh(db_course)
    return {"msg": "SUCCESS"}

# Eliminar un curso existente
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()
    return {"msg": "SUCCESS"}
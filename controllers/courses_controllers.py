from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

def get_user_courses(user_id: int, db: Session = Depends(get_db)):
    print("get_user_courses") #TODO Implementar la función para obtener los cursos de un usuario

def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    print("create_course") #TODO Implementar la función para crear un curso

def update_course(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    print("update_course") #TODO Implementar la función para actualizar un curso

def delete_course(course_id: int, db: Session = Depends(get_db)):
    print("delete_course") #TODO Implementar la función para eliminar un curso


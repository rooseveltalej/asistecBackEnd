from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

def get_user_activities(user_id: int, db: Session = Depends(get_db)):
    print("get_user_activities") #TODO Implementar la función para obtener las actividades de un usuario

def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    print("create_activity") #TODO Implementar la función para crear una actividad

def update_activity(activity_id: int, activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    print("update_activity") #TODO Implementar la función para actualizar una actividad

def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    print("delete_activity") #TODO Implementar la función para eliminar una actividad


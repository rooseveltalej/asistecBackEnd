from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db


def get_user_events(user_id: int, db: Session = Depends(get_db)):
    db_events = db.query(models.Event).filter(models.Event.user_id == user_id).all()
    return db_events

def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)): #Función para crear un evento, esta función se importa en el archivo events_routes.py
    new_event = models.Event(**event.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return {"msg": "SUCCESS"}
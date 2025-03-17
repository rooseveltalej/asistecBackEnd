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

def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)): #Función para actualizar un evento, esta función se importa en el archivo events_routes.py
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if db_event:
        db_event.event_title = event.event_title
        db_event.event_description = event.event_description
        db_event.event_date = event.event_date
        db_event.event_start_hour = event.event_start_hour
        db_event.event_final_hour = event.event_final_hour
        db_event.notification_datetime = event.notification_datetime
        db_event.all_day = event.all_day
        db.commit()
        return {"msg": "SUCCESS"}
    else:
        raise HTTPException(status_code=404, detail="Evento no encontrado") #Si no se encuentra el evento, se devuelve un error 404
    

# Falta implementar la función para eliminar un evento
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

def get_user_events(user_id: int, db: Session = Depends(get_db)):
    db_events = db.query(models.Event).filter(models.Event.user_id == user_id).all()
    return db_events

def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    new_event = models.Event(**event.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return JSONResponse(
        content={"msg": "SUCCESS", "event_id": new_event.event_id},
        status_code=status.HTTP_201_CREATED
    )

def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    for key, value in event.model_dump().items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return {"msg": "SUCCESS"}
    

def delete_event_by_id(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    db.delete(db_event)
    db.commit()

    return JSONResponse(
        content={"msg": "SUCCESS"},
        status_code=status.HTTP_200_OK
    )
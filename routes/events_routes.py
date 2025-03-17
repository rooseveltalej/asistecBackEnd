from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from controllers.events_controllers import create_event, get_user_events, update_event

event_router = APIRouter(prefix="/api/events", tags=["Events"])

@event_router.get("/user_events")
def get_user_events_route(user_id: int, db: Session = Depends(get_db)):
    return get_user_events(user_id, db)

@event_router.post("/event_create", status_code=status.HTTP_201_CREATED)
def create_event_route(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return create_event(event, db)

@event_router.put("/event_update")
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    return update_event(event_id, event, db)

@event_router.delete("/event_delete")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    return {"msg": "SUCCESS"} #TODO: Falta implementar la función para eliminar un evento
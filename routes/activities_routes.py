from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from controllers.activities_controllers import create_activity, get_user_activities, update_activity, delete_activity

activity_router = APIRouter(prefix="/api/activities", tags=["Activities"])

@activity_router.get("/user_activities")
def get_user_activities_route(user_id: int, db: Session = Depends(get_db)):
    return get_user_activities(user_id, db)

@activity_router.post("/activity_create", status_code=status.HTTP_201_CREATED)
def create_activity_route(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return create_activity(activity, db)

@activity_router.put("/activity_update")
def update_activity_route(activity_id: int, activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return update_activity(activity_id, activity, db)

@activity_router.delete("/activity_delete")
def delete_activity_route(activity_id: int, db: Session = Depends(get_db)):
    return delete_activity(activity_id, db)
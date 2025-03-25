from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers.users_controllers import create_user, login_user

user_router = APIRouter(prefix="/api/users", tags=["Users"])

@user_router.post("/user_create/", status_code=status.HTTP_201_CREATED)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@user_router.get("/user_login/")
def login_user_route(mail: str, password: str, db: Session = Depends(get_db)):
    return login_user(mail, password, db)
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers.users_controllers import create_user, login_user, get_user_next_activities
from interfaces.auth_factory import AuthFactory

user_router = APIRouter(prefix="/api/users", tags=["Users"])

@user_router.post("/user_create", status_code=status.HTTP_201_CREATED)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        provider = AuthFactory.get_auth_provider(user.mail)
    except ValueError:
        raise HTTPException(status_code=400, detail="Dominio de correo no permitido")

    return provider.create_user(user, db)


@user_router.post("/user_login")
def login_user_route(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        provider = AuthFactory.get_auth_provider(user.mail)
    except ValueError:
        raise HTTPException(status_code=400, detail="Dominio de correo no permitido")

    return provider.login(user, db)

@user_router.get("/next_activities", response_model=list)
def get_user_next_activities_route(user_id: int, db: Session = Depends(get_db)):
    return get_user_next_activities(user_id, db)

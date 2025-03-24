from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.mail == user.mail).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    user_data = user.model_dump(exclude={"password"})
    new_user = models.User(**user_data, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Obtener canal principal del área del usuario
    main_channel = db.query(models.Channel).filter(models.Channel.area_id == new_user.area_id).first()
    if main_channel:
        subscription = models.Subscription(
            user_id=new_user.user_id,
            channel_id=main_channel.channel_id,
            is_admin=False,
            is_favorite=True
        )
        db.add(subscription)

    # Obtener canales informativos (de áreas con is_major = False)
    informative_area_ids = db.query(models.Area.area_id).filter(models.Area.is_major == False).subquery()
    informative_channels = db.query(models.Channel).filter(models.Channel.area_id.in_(informative_area_ids)).all()

    for channel in informative_channels:
        subscription = models.Subscription(
            user_id=new_user.user_id,
            channel_id=channel.channel_id,
            is_admin=False,
            is_favorite=True
        )
        db.add(subscription)

    db.commit()

    return {"msg": "SUCCESS"}

def login_user(mail: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.mail == mail).first()
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "user_id": db_user.user_id,
        "email": db_user.mail,
        "full_name": f"{db_user.name} {db_user.lastname}"
    }
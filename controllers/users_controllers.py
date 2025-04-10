# Standard library
import calendar
import json
from datetime import date, datetime, timedelta

# Third-party packages
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Internal modules
import models
import schemas
from database import get_db


# Mapea días a números (Monday = 0)
weekday_map = {day.lower(): i for i, day in enumerate(calendar.day_name)}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.mail == user.mail).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

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

    # ✅ Corregido: select() explícito en lugar de subquery()
    informative_area_ids = select(models.Area.area_id).where(models.Area.is_major == False)
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

    return JSONResponse(
        content={"msg": "SUCCESS", "user_id": new_user.user_id},
        status_code=status.HTTP_201_CREATED
    )

def login_user(user: schemas.UserLogin, db: Session):
    db_user = db.query(models.User).filter(models.User.mail == user.mail).first()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")    
    
    # Check if the user is active
    if not db_user.is_active:
        raise HTTPException(status_code=401, detail="Inactive")

    return {
        "user_id": db_user.user_id,
        "email": db_user.mail,
        "full_name": f"{db_user.name} {db_user.lastname}",
        "area": db_user.area.area_name
    }

def get_next_occurrence(start_date: date, final_date: date, schedule: dict) -> tuple | None:
    today = date.today()

    for day_offset in range(0, 14):  # Ver próximos 14 días
        check_date = today + timedelta(days=day_offset)
        if not (start_date <= check_date <= final_date):
            continue

        weekday = check_date.weekday()
        for entry in schedule.values():
            scheduled_day = weekday_map.get(entry["date"].lower())
            if scheduled_day == weekday:
                return check_date, entry["start_time"]
    return None


def get_user_next_activities(user_id: int, db: Session = Depends(get_db)):
    today = date.today()
    upcoming = []

    # Eventos
    events = db.query(models.Event).filter(
        models.Event.user_id == user_id,
        models.Event.event_date >= today
    ).order_by(models.Event.event_date.asc()).all()

    for e in events:
        upcoming.append({
            "id": e.event_id,
            "type": "event",
            "title": e.event_title,
            "date": e.event_date,
            "start_time": e.event_start_hour,
            "location": e.location
        })

    # Actividades
    activities = db.query(models.Activities).filter(
        models.Activities.user_id == user_id
    ).all()

    for a in activities:
        schedule = json.loads(a.schedule)
        next_occurrence = get_next_occurrence(a.activity_start_date, a.activity_final_date, schedule)
        if next_occurrence:
            occ_date, start_time = next_occurrence
            if occ_date >= today:
                upcoming.append({
                    "id": a.activity_id,
                    "type": "activity",
                    "title": a.activity_title,
                    "date": occ_date,
                    "start_time": start_time,
                    "location": a.location
                })

    # Cursos
    courses = db.query(models.Course).filter(
        models.Course.user_id == user_id
    ).all()

    for c in courses:
        schedule = json.loads(c.schedule)
        next_occurrence = get_next_occurrence(c.course_start_date, c.course_final_date, schedule)
        if next_occurrence:
            occ_date, start_time = next_occurrence
            if occ_date >= today:
                upcoming.append({
                    "id": c.course_id,
                    "type": "course",
                    "title": c.course_title,
                    "date": occ_date,
                    "start_time": start_time,
                    "location": c.location
                })

    # Ordenar por fecha y hora
    upcoming.sort(key=lambda x: (x["date"], datetime.strptime(x["start_time"], "%H:%M")))

    return upcoming[:3]
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

# Obtener todas las áreas
def get_areas(db: Session = Depends(get_db)):
    return db.query(models.Area).all()

# Crear una nueva área y su canal asociado automáticamente
def create_area(area: schemas.AreaBase, db: Session = Depends(get_db)):
    existing = db.query(models.Area).filter_by(area_name=area.area_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Area with this name already exists")

    new_area = models.Area(**area.model_dump())
    db.add(new_area)
    db.commit()
    db.refresh(new_area)

    # Crear un canal asociado a la nueva área
    new_channel = models.Channel(
        channel_name=f"Canal de {new_area.area_name}",
        area_id=new_area.area_id
    )
    db.add(new_channel)
    db.commit()

    return new_area

# Obtener las áreas donde el is_major sea True
def get_major_areas(db: Session = Depends(get_db)):
    return db.query(models.Area).filter_by(is_major=True).all()
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

area_router = APIRouter(prefix="/api/areas", tags=["Areas"])

# Obtener todas las áreas
@area_router.get("/", response_model=list[schemas.AreaResponse])
def get_areas(db: Session = Depends(get_db)):
    areas = db.query(models.Area).all()
    return areas

# Crear una nueva área y un canal asociado automáticamente
@area_router.post("/create", response_model=schemas.AreaResponse, status_code=status.HTTP_201_CREATED)
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
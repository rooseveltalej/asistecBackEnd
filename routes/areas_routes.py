from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers.areas_controllers import get_areas, create_area

area_router = APIRouter(prefix="/api/areas", tags=["Areas"])

# Obtener todas las áreas
@area_router.get("/", response_model=list[schemas.AreaResponse])
def get_areas_route(db: Session = Depends(get_db)):
    return get_areas(db)

# Crear una nueva área y canal asociado automáticamente
@area_router.post("/create", response_model=schemas.AreaResponse, status_code=status.HTTP_201_CREATED)
def create_area_route(area: schemas.AreaBase, db: Session = Depends(get_db)):
    return create_area(area, db)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers.professors_controllers import create_professor, get_all_professors

professor_router = APIRouter(prefix="/api/professors", tags=["Professors"])

@professor_router.get("/", response_model=list[schemas.ProfessorResponse])
def get_all_professors_route(db: Session = Depends(get_db)):
    return get_all_professors(db)

@professor_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_professor_route(professor: schemas.ProfessorBase, db: Session = Depends(get_db)):
    return create_professor(professor, db)
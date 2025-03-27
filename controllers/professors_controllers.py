
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

def get_all_professors(db: Session = Depends(get_db)):
    professors = db.query(models.Professor).all()
    return professors

# Crear un nuevo profesor
def create_professor(professor: schemas.ProfessorBase, db: Session = Depends(get_db)):
    new_prof = models.Professor(**professor.model_dump())
    db.add(new_prof)
    db.commit()
    db.refresh(new_prof)
    return {"msg": "SUCCESS", "professor_id": new_prof.professor_id}
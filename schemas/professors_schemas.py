from pydantic import BaseModel


# Professor Schemas
class ProfessorBase(BaseModel):
    professor_name: str
    professor_lastname: str

class ProfessorResponse(ProfessorBase):
    professor_id: int
    class Config:
        from_attributes = True

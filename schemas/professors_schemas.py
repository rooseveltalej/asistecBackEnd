from pydantic import BaseModel, ConfigDict

# Professor Schemas
class ProfessorBase(BaseModel):
    professor_name: str
    professor_lastname: str

class ProfessorResponse(ProfessorBase):
    professor_id: int
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date

class UserBase(BaseModel):
    name: str
    lastname: str
    mail: EmailStr
    area_id: int
    carnet_number: str            # ← Nuevo campo
    gender: str                   # ← Nuevo campo (por ejemplo: "M", "F", "Otro")
    birth_date: date              # ← Nuevo campo

class UserLogin(BaseModel):
    mail: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserListResponse(BaseModel):
    user_id: int
    name: str
    lastname: str
    mail: str
    carnet_number: str
    gender: str
    birth_date: date
    area_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

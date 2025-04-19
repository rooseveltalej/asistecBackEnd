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

class UserResponse(UserBase):
    user_id: int
    full_name: str

    model_config = ConfigDict(from_attributes=True)

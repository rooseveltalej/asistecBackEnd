from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    name: str
    lastname: str
    mail: EmailStr
    area_id: int

class UserLogin(BaseModel):
    mail: EmailStr
    password: str  

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    full_name: str

    model_config = ConfigDict(from_attributes=True)

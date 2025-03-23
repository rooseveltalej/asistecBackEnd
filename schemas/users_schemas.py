from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    lastname: str
    mail: EmailStr
    area_id: int  

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    full_name: str

    class Config:
        from_attributes = True

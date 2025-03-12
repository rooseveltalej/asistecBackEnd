from pydantic import BaseModel, EmailStr

# User Schemas
class UserBase(BaseModel):
    name: str
    lastname: str
    mail: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    full_name: str
    class Config:
        from_attributes = True
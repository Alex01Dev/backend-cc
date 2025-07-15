from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    status: str

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: str
    registration_date: datetime

    class Config:
        from_attributes = True  # replaces orm_mode

class UserLogin(BaseModel):
    username: str
    password: str

class UserSimple(BaseModel):
    id: int
    username: str
    status: str

    class Config:
        from_attributes = True

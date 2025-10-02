from pydantic import BaseModel, EmailStr
import uuid


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    name: str
    surname: str
    pwd: str


class UserLogin(BaseModel):
    username: str
    pwd: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    name: str

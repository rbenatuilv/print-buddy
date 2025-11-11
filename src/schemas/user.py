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
    email: EmailStr
    username: str
    name: str
    surname: str
    balance: float
    credit_limit: float


class UserAdminRead(UserRead):
    id: uuid.UUID


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    name: str | None = None
    surname: str | None = None


class UserChangePassword(BaseModel):
    current_pwd: str
    new_pwd: str


class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr


class UserEmailRequest(BaseModel):
    email: EmailStr


class UserPwdReset(BaseModel):
    new_pwd: str
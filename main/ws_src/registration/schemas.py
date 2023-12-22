import uuid

from pydantic import BaseModel, EmailStr


class UserRegisterData(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str


class UserLoginData(BaseModel):
    username: str
    password: str
from pydantic import BaseModel, EmailStr
from ws_src.common.choices import BaseUserTypes

class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str = BaseUserTypes.DEFAULT_USER

class UserLoginSchema(BaseModel):
    username: str
    password: str
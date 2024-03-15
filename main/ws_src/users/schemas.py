from pydantic import BaseModel
from ws_src.users.models import User


class UserSchema(BaseModel):
    user: User
    text: str

    class Config:
        arbitrary_types_allowed = True

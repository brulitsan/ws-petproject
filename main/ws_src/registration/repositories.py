import os

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .schemas import UserRegisterSchema


def create_user(data: UserRegisterSchema):
    user_model = get_user_model()
    user_properties = data.model_dump()
    user_properties["password"] = make_password(data.password)
    user = user_model(**user_properties)
    user.save()
    return user


def decode_refresh_token(refresh_token: str, secret_key: str):
    return jwt.decode(
        refresh_token,
        key=secret_key,
        options={"verify_exp": False},
        algorithms=[os.environ.get("ALGORITHM")],
    )


def encode_access_token(payload: dict, secret_key: str):
    return jwt.encode(
        payload,
        secret_key,
        algorithm=os.environ.get("ALGORITHM")
    )

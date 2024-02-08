import os

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .schemas import UserRegisterSchema


def create_user(user_register_schema: UserRegisterSchema):
    user_model = get_user_model()
    user_register_schema.password = make_password(user_register_schema.password)
    user = user_model(**user_register_schema.model_dump())
    user.save()
    return user


def decode_refresh_token(refresh_token: str, secret_key: str):
    print(jwt.decode(
        refresh_token,
        key=secret_key,
        options={"verify_exp": False},
        algorithms=[os.environ.get("ALGORITHM")],
    )
    )
    return jwt.decode(
        refresh_token,
        key=secret_key,
        options={"verify_exp": False},
        algorithms=[os.environ.get("ALGORITHM")],
    )


def encode_access_token(payload: dict, secret_key: str):
    print(jwt.encode(
        payload,
        secret_key,
        algorithm=os.environ.get("ALGORITHM")
    ))
    return jwt.encode(
        payload,
        secret_key,
        algorithm=os.environ.get("ALGORITHM")
    )

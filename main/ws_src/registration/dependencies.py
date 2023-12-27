import os
from datetime import datetime, timedelta
from django.contrib.auth import authenticate as auth

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .schemas import UserRegisterData

from main.settings import ALGORITHM, SECRET_KEY


def generate_token(
        user,
        minutes,
):
    payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=int(minutes))
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=os.environ.get('ALGORITHM')
    )
    return token


def create_user(data: UserRegisterData):
    User = get_user_model()
    user = User(
        username=data.username,
        password=make_password(data.password),
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name
    )
    user.save()
    return user


def authenticate(
        request,
        username,
        password
):
    user = auth(request, username=username, password=password)
    if user is None:
        return None
    return user

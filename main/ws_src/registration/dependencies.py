import os
from datetime import datetime, timedelta
from django.contrib.auth import authenticate as auth

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from rest_framework import status

from main import settings
from ws_src.users.models import User
from .schemas import UserRegisterData

from main.settings import ALGORITHM, SECRET_KEY

def generate_token(
        user,
        minutes,
):
    payload = {
        'id': str(user.id),
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
        last_name=data.last_name,
        role=data.role
    )
    user.save()
    return user


def is_authenticated(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[os.environ.get('ALGORITHM')])
            user_id = payload['id']
            user = User.objects.get(id=user_id)
            return user

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None
    # return AnonymousUser
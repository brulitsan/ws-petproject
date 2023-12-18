import os
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.contrib.auth.hashers import make_password

from ws_src.users.models import User


def generate_token(
        user,
        minutes,
):
    payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=minutes)
    }
    token = jwt.encode(
        payload,
        os.environ.get('SECRET_KEY'),
        algorithm=os.environ.get('ALGORITHM')
    )
    return token


def create_user(request):
    data = request.data
    user = User(
        id=uuid4(),
        username=data['username'],
        password=make_password(data['password']),
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    user.save()
    return user

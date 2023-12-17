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
        'django-insecure-nn+8rknd1qy2fj7eju#(q=5vts3%fah--hg7j@1)1%3!go6z6%',
        algorithm='HS256'
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
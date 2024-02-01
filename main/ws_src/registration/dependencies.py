import os
from datetime import timedelta
from http.client import HTTPException
from django.utils import timezone
import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from rest_framework import status

from django.conf import settings


from ws_src.users.models import User
from ws_src.registration.schemas import UserRegisterSchema


def generate_token(
    user,
    minutes,
):
    payload = {
        "id": str(user.id),
        "exp": timezone.now() + timedelta(minutes=int(minutes)),
    }
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=os.environ.get("ALGORITHM")
    )
    return token


def create_user(data: UserRegisterSchema):
    User = get_user_model()
    user_properties = data.model_dump()
    user_properties["password"] = make_password(data.password)
    user = User(**user_properties)
    user.save()
    return user


def is_authenticated(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is not None:
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[os.environ.get("ALGORITHM")]
            )
            user_id = payload["id"]
            user = User.objects.get(id=user_id)
            return user

        except jwt.ExpiredSignatureError:
            return HTTPException(status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return HTTPException(status=status.HTTP_401_UNAUTHORIZED)
    return AnonymousUser

import os
from datetime import timedelta
from http.client import HTTPException

import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework import status
from ws_src.users.models import User


def generate_token(
    minutes: str,
    user: User = None,
):
    payload = {
        "id": str(user.id),
        "exp": timezone.now() + timedelta(minutes=int(minutes)),
    }
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=os.environ.get("ALGORITHM")
    )
    return token


def is_authenticated(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return AnonymousUser
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
        return HTTPException(status=status.HTTP_403_FORBIDDEN)

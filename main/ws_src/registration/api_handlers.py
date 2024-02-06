import os

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import exceptions, generics, status
from rest_framework.response import Response

from .dependencies import generate_token
from .repositories import (create_user, decode_refresh_token,
                           encode_access_token)
from .schemas import UserLoginSchema, UserRegisterSchema
from .serialiser import LoginSerializer, UserSerialiser


class RegisterUserView(
    generics.GenericAPIView,
):
    serializer_class = UserSerialiser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = UserRegisterSchema(**serializer.validated_data)
        user = create_user(user_data)
        access_token = generate_token(user=user, minutes=settings.ACCESS_TOKEN_LIFE)
        refresh_token = generate_token(user=user, minutes=settings.REFRESH_TOKEN_LIFE)
        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = UserLoginSchema(**serializer.validated_data)
        user = authenticate(
            request,
            username=user_data.username,
            password=user_data.password,
        )
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid username or password")
        access_token = generate_token(user=user, minutes=settings.ACCESS_TOKEN_LIFE)
        refresh_token = generate_token(user=user, minutes=settings.REFRESH_TOKEN_LIFE)
        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_200_OK,
        )


class RefreshTokenView(generics.GenericAPIView):
    SECRET_KEY = os.environ.get("SECRET_KEY")

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        payload = decode_refresh_token(refresh_token, self.SECRET_KEY)
        new_access_token = encode_access_token(payload, self.SECRET_KEY)
        return Response(
            {'access_token': new_access_token},
            status=status.HTTP_200_OK
        )

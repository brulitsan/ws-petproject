import os
from asyncio import exceptions

import jwt
from django.contrib.auth import authenticate
from rest_framework import status, generics, exceptions
from rest_framework.response import Response

from .schemas import UserRegisterData, UserLoginData

from main.settings import ACCESS_TOKEN_LIFE, REFRESH_TOKEN_LIFE
from .dependencies import create_user, generate_token
from .serialiser import UserSerialiser, LoginSerializer


class RegisterUserView(
    generics.GenericAPIView,
):
    def post(self, request):
        serializer = UserSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = UserRegisterData(**serializer.validated_data)
            user = create_user(user_data)
            access_token = generate_token(user=user, minutes=ACCESS_TOKEN_LIFE)
            refresh_token = generate_token(user=user, minutes=REFRESH_TOKEN_LIFE)
            return Response({'access_token': access_token, 'refresh_token': refresh_token},
                         status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = UserLoginData(**serializer.validated_data)
        user = authenticate(
            request,
            username=user_data.username,
            password=user_data.password,
        )
        if user is not None:
            access_token = generate_token(user=user, minutes=ACCESS_TOKEN_LIFE)
            refresh_token = generate_token(user=user, minutes=REFRESH_TOKEN_LIFE)
            return Response({'access_token': access_token, 'refresh_token': refresh_token},
                             status=status.HTTP_200_OK)
        else:
            raise exceptions.AuthenticationFailed('Invalid username or password')


class RefreshTokenView(generics.GenericAPIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        payload = jwt.decode(refresh_token,
                             key=os.environ.get('SECRET_KEY'),
                             options={"verify_exp": False},
                             algorithms=[os.environ.get('ALGORITHM')])
        new_access_token = jwt.encode(
            payload,
            os.environ.get('SECRET_KEY'),
            algorithm=os.environ.get('ALGORITHM'))
        return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)

import os
from asyncio import exceptions

import jwt
from django.contrib.auth import authenticate
from rest_framework import status, generics, exceptions
from rest_framework.response import Response

from .schemas import UserRegisterSchema, UserLoginSchema

from django.conf import settings
from .dependencies import create_user, generate_token
from .serialiser import UserSerialiser, LoginSerializer


class RegisterUserView(
    generics.GenericAPIView,
):
    serializer_class = UserSerialiser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = UserRegisterSchema(**serializer.validated_data)
        user = create_user(user_data)
        print(user)
        access_token = generate_token(user=user, minutes=settings.ACCESS_TOKEN_LIFE)
        refresh_token = generate_token(user=user, minutes=settings.REFRESH_TOKEN_LIFE)
        return Response({'access_token': access_token, 'refresh_token': refresh_token},
                         status=status.HTTP_201_CREATED)


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
        if user is not None:
            access_token = generate_token(user=user, minutes=settings.ACCESS_TOKEN_LIFE)
            refresh_token = generate_token(user=user, minutes=settings.REFRESH_TOKEN_LIFE)
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

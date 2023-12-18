import os

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .dependencies import create_user, generate_token
from .serialiser import UserSerialiser


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(request)
        access_token = generate_token(user, 15)
        refresh_token = generate_token(user, 3600)
        return f"access: {access_token}, refresh: {refresh_token}"

    def refresh_access_token(self, refresh_token):
        payload = jwt.decode(refresh_token, options={"verify_exp": False})
        new_access_token = jwt.encode(
            payload,
            os.environ.get('SECRET_KEY'),
            algorithm=os.environ.get('ALGORITHM'))
        return new_access_token


class LoginUserView(APIView):
    def post(self, request):
        id = request.data.get('id')
        password = request.data.get('password')
        try:
            user = User.objects.get(id=id)
            if user.check_password(password):
                access_token = generate_token(user.id, 15)
                refresh_token = generate_token(user.id, 3600)
                return Response({'access_token': access_token, 'refresh_token': refresh_token},
                                status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except User is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ws_src.users.models import User
from .dependencies import create_user, generate_token
from .serialiser import UserSerialiser


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(request)
        assign_token_view = AssignTokenView()
        assign_token_view.post(request)
        return Response({'message': 'Данные получены'}, status=status.HTTP_200_OK)


class AssignTokenView(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data['id'])
        access_token = generate_token(user, 15)
        refresh_token = generate_token(user, 24*60)
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        return Response(status=status.HTTP_200_OK)

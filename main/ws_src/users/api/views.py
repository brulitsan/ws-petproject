from asgiref.sync import async_to_sync
from django.http import HttpRequest
from rest_framework import generics
from rest_framework.response import Response
from ws_src.users.api.serializer import UserTextSerializer
from ws_src.users.brocker import send_currency_info_request
from ws_src.users.permissions import IsAdmin


class UserView(generics.GenericAPIView):
    serializer_class = UserTextSerializer
    permission_classes = [IsAdmin, ]

    def post(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        send_one_sync = async_to_sync(send_currency_info_request)
        send_one_sync(text)
        return Response({'text': text})

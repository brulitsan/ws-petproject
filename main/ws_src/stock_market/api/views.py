from ws_src.stock_market.api.serialiser import (
    AutoOperationsOrderSerializer,
    OrderSerializer,
    UserTextSerializer,
)
from ws_src.stock_market.brocker import send_currency_info_request
from ws_src.stock_market.database import auto_operations
from ws_src.stock_market.models import Product
from ws_src.stock_market.schemas import AutoOperationsOrderSchema, OrderSchema
from ws_src.users.database import update_user_balance
from ws_src.users.permissions import IsAdmin, IsUser

from django.http import HttpRequest
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class BuyItemViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsUser]

    def perform_create(self, serializer: OrderSerializer) -> None:
        user = self.request.current_user
        order_dto = OrderSchema(user=user, **serializer.validated_data)

        order_dto.update_quantity()
        order_status = update_user_balance(user=user, order_dto=order_dto)
        order_dto.status = order_status
        serializer.save(**order_dto.model_dump())


class AutomaticOperationsViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = AutoOperationsOrderSerializer
    permission_classes = [IsUser]

    def perform_create(self, serializer: OrderSerializer) -> None:
        user = self.request.current_user
        order_dto = AutoOperationsOrderSchema(user=user, **serializer.validated_data)

        order_dto.update_quantity()
        order_status = auto_operations(user=user, order_dto=order_dto)
        order_dto.status = order_status
        serializer.save(**order_dto.model_dump())


class GetCurrencyInfo(generics.GenericAPIView):
    serializer_class = UserTextSerializer
    permission_classes = [IsAdmin]

    def post(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        send_currency_info_request(text)
        return Response({'added': text})

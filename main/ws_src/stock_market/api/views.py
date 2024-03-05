import os

import requests
from django.http import HttpRequest
from rest_framework import generics, mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ws_src.stock_market.api.serialiser import OrderSerializer, UserTextSerializer
from ws_src.stock_market.brocker import send_currency_info_request
from ws_src.stock_market.database import update_or_create_products
from ws_src.stock_market.models import Product
from ws_src.stock_market.schemas import OrderSchema, ProductSchema
from ws_src.users.database import update_user_balance
from ws_src.users.permissions import IsAdmin, IsUser

# from ws_src.stock_market.tasks import consume_crypto_info


class StockMarketViewSet(viewsets.ViewSet):
    schema = ProductSchema

    def list(self, request: Request) -> Response:
        url = os.environ.get("GET_COINS_URL")
        response = requests.get(url)
        crypto_list = response.json()
        update_or_create_products(crypto_list)
        return Response(crypto_list)


class BuyItemViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsUser,)

    def perform_create(self, serializer: OrderSerializer) -> None:
        user = self.request.current_user
        order_dto = OrderSchema(user=user, **serializer.validated_data)
        serializer.save(**order_dto.model_dump())

        update_user_balance(user, order_dto)


# class AutomaticOperationsViewSet(GenericViewSet)


class GetCurrencyInfo(generics.GenericAPIView):
    serializer_class = UserTextSerializer
    permission_classes = [IsAdmin, ]

    def post(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        send_currency_info_request(text)
        return Response({'text': text})

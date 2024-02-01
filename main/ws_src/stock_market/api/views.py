import os

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

import requests
from rest_framework.response import Response

from ws_src.users.permissions import IsUser
from ws_src.users.database import update_or_create_user_product, update_user_balance

from ws_src.stock_market.models import Product, ProductCategories
from ws_src.stock_market.api.serialiser import OrderSerializer
from ws_src.stock_market.schemas import ProductSchema, OrderSchema


class StockMarketViewSet(viewsets.ViewSet):
    schema = ProductSchema

    def list(self, request):
        url = os.environ.get('GET_COINS_URL')
        response = requests.get(url)
        crypto_list = response.json()
        self.update_or_create_products(crypto_list)
        return Response(crypto_list)

    @staticmethod
    def update_or_create_products(product_data):
        for item in product_data:
            item = ProductSchema(**item)
            category, _ = ProductCategories.objects.get_or_create(name=item.symbol)
            product, created = Product.objects.update_or_create(id=item.id, defaults=item.model_dump())


class BuyItemViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsUser,)

    def perform_create(self, serializer):
        user = self.request.current_user
        order_dto = OrderSchema(user=user, **serializer.validated_data)
        serializer.save(**order_dto.model_dump())

        update_user_balance(user, order_dto)
        update_or_create_user_product(user, order_dto)

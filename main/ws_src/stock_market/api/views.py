import os

from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

import requests
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from ws_src.users.permissions import IsUser
from ws_src.users.database import update_or_create_user_product, update_user_balance
from ws_src.stock_market.database import update_or_create_product

from ws_src.stock_market.models import Product, ProductCategories
from ws_src.stock_market.api.serialiser import OrderSerializer
from ws_src.stock_market.schemas import ProductModel, OrderDto


class StockMarketView(APIView):

    def get(self, request):
        url = os.environ.get('GET_COINS_URL')
        response = requests.get(url)
        crypto_list = response.json()
        self.update_or_create_products(crypto_list)
        return Response(crypto_list)

    @staticmethod
    def update_or_create_products(product_data: list[ProductModel]):
        with transaction.atomic():
            for item in product_data:
                item = ProductModel(**item)
                category, _ = ProductCategories.objects.get_or_create(name=item.symbol)
                product, created = update_or_create_product(
                    item.id,
                    category,
                    item.lastPrice,
                    item.highPrice,
                    item.lowPrice
                )
                if created:
                    print(f'Создан новый продукт: {product}')
                else:
                    print(f'Обновлен продукт: {product}')


class BuyItemViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsUser,)

    def perform_create(self, serializer):
        user = self.request.current_user
        order_dto = OrderDto(user=user, **serializer.validated_data)
        serializer.save(**order_dto.model_dump())

        update_user_balance(user, order_dto)
        update_or_create_user_product(user, order_dto)






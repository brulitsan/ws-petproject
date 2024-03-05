from collections import OrderedDict
from decimal import Decimal

from rest_framework import serializers
from ws_src.stock_market.database import get_quantity, processing_quantity
from ws_src.stock_market.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ('user',)

        fields = ["user", "product", "transaction_price", "type", "quantity"]

    quantity = serializers.SerializerMethodField("get_quantity_value")

    def get_quantity_value(self, obj: Order) -> Decimal:
        return get_quantity(obj)

    def paste_quantity_to_order(self, product: OrderedDict) -> OrderedDict:
        return processing_quantity(product)

    def to_internal_value(self, order: OrderedDict) -> OrderedDict:
        data = super().to_internal_value(order)
        order_quantity = self.paste_quantity_to_order(data)
        print(order_quantity)
        return order_quantity


class UserTextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)

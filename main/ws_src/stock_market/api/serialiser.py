from collections import OrderedDict
from decimal import Decimal

from rest_framework import serializers
from ws_src.stock_market.database import get_quantity, processing_quantity
from ws_src.stock_market.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["user", "product", "transaction_price", "type", "quantity"]

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.SerializerMethodField("get_quantity_value")

    def get_quantity_value(self, obj: Order) -> Decimal:
        return get_quantity(obj)

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        return processing_quantity(attrs)

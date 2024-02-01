from rest_framework import serializers

from ws_src.stock_market.database import get_quantity, validate
from ws_src.stock_market.models import Product, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["user_id", "product", "transaction_price", "type", "quantity"]

    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.SerializerMethodField("get_quantity_value")

    def get_quantity_value(self, obj):
        return get_quantity(obj)

    def validate(self, attrs):
        return validate(attrs)

from rest_framework import serializers

from ws_src.stock_market.models import Product, Order
import uuid


class OrderSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['user_id', 'product_id', 'transaction_price', 'type', 'quantity']

    def get_quantity(self, obj):
        product_price = Product.objects.get(id=obj.product_id).price
        return obj.transaction_price / float(product_price)

    def validate(self, attrs):
        product = Product.objects.get(id=attrs['product_id'])
        attrs['quantity'] = attrs['transaction_price'] / product.price
        return attrs



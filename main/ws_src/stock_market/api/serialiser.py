from rest_framework import serializers
from ws_src.stock_market.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ('user', 'status', 'quantity', 'currency_price')

        fields = ["user",
                  "product",
                  "transaction_price",
                  "type",
                  "quantity",
                  "status",
                  "currency_price"
                  ]


class AutoOperationsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ('user', 'status', 'quantity')

        fields = ["user",
                  "product",
                  "transaction_price",
                  "type",
                  "quantity",
                  "status",
                  "currency_price"
                  ]


class UserTextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)

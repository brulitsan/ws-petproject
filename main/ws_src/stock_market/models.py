import uuid
from datetime import datetime
from decimal import Decimal

from django.db import models
from ws_src.common.choices import BaseOrderType, BaseProductType
from ws_src.common.models import BaseModel


class ProductCategories(BaseModel):
    name = models.CharField(max_length=30, choices=BaseProductType.choices)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return (
            f"product - {self.name} | parent - {self.parent}"
            if self.parent
            else self.name
        )


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    id: str = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    symbol: str = models.CharField(max_length=100, unique=True)
    last_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    high_price: Decimal = models.DecimalField(max_digits=10, decimal_places=3)
    low_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    product: str = models.ForeignKey(Product, on_delete=models.PROTECT)
    user: uuid.UUID = models.ForeignKey("users.User", on_delete=models.PROTECT)
    transaction_price: Decimal = models.DecimalField(max_digits=10, decimal_places=3)
    quantity: Decimal = models.DecimalField(max_digits=10, decimal_places=4)
    type: str = models.CharField(choices=BaseOrderType.choices, max_length=30)
    created_at: datetime = models.DateTimeField(auto_now_add=True)

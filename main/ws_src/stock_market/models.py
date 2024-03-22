from decimal import Decimal

import uuid
from ws_src.common.choices import BaseOrderStatus, BaseOrderType, BaseProductType
from ws_src.common.models import BaseModel

from django.db import models


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

    id: uuid.UUID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    symbol: str = models.CharField(max_length=100, unique=True)
    last_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    high_price: Decimal = models.DecimalField(max_digits=10, decimal_places=3)
    low_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)


class Order(BaseModel):
    product: str = models.ForeignKey(Product, on_delete=models.PROTECT)
    user: uuid.UUID = models.ForeignKey("users.User", on_delete=models.PROTECT)
    transaction_price: Decimal = models.DecimalField(max_digits=10, decimal_places=3)
    quantity: Decimal = models.DecimalField(max_digits=10, decimal_places=4)
    type: str = models.CharField(choices=BaseOrderType.choices, max_length=30)
    status = models.CharField(choices=BaseOrderStatus.choices, max_length=30)
    currency_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.currency_price is None:
            self.currency_price = self.product.last_price
        super().save(*args, **kwargs)

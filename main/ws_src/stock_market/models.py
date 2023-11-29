import uuid

from django.db import models
from ws_src.common.models import BaseOrderType, ProductCategories


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey(ProductCategories, on_delete=models.PROTECT, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=3)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"product - {self.name}"


class Order(models.Model):
    product_id: models.OneToOneField("stock_market.Product", on_delete=models.PROTECT)
    user_id: models.OneToOneField("users.User", on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=3, max_digits=3)
    currency = models.CharField(max_length=20)
    type = models.CharField(choices=BaseOrderType.choices(), max_length=30)

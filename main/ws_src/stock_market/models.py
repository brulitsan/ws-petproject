from django.db import models
from ws_src.common.choices import BaseOrderType, BaseProductType
from ws_src.common.models import BaseModel


class ProductCategories(BaseModel):
    name = models.CharField(max_length=30, choices=BaseProductType.choices)
    parent = models.ForeignKey("self", on_delete=models.PROTECT,  null=True, blank=True)

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

    id = models.CharField(primary_key=True, editable=False)
    name = models.ForeignKey(ProductCategories, on_delete=models.PROTECT, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=3)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    product_id = models.CharField(max_length=100)
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    transaction_price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    type = models.CharField(choices=BaseOrderType.choices, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

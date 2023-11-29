from enum import Enum

from django.db import models

# Create your models here.


class BaseUserTypes(Enum):
    DEFAULT_USER = "Пользователь"
    ANALYST = "Аналитик"
    ADMIN = "Администратор"

    @classmethod
    def choices(cls):
        return [(user.value, user.name) for user in cls]


class BaseOrderType(Enum):
    PURCHASE = "Покупка"
    SALE = "Продажа"

    @classmethod
    def choices(cls):
        return [(order.value, order.name) for order in cls]


class BaseProductType(Enum):
    CRYPTOCURRENCY = "криптовалюта"
    STOCK = "акции"
    FUTURES = "фьючерсы"
    BONDS = "облигации"

    @classmethod
    def choices(cls):
        return [(order.value, order.name) for order in cls]


class ProductCategories(models.Model):
    name = models.CharField(max_length=30, choices=BaseProductType.choices())
    parent = models.ForeignKey("self", on_delete=models.PROTECT)

    def __str__(self):
        return (
            f"product - {self.name} | parent - {self.parent}"
            if self.parent
            else self.name
        )

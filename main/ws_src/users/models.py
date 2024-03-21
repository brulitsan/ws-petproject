import uuid
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from ws_src.common.choices import BaseUserTypes
from ws_src.common.models import BaseModel


class User(AbstractUser, BaseModel):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        choices=BaseUserTypes.choices, max_length=20, default=BaseUserTypes.DEFAULT_USER
    )
    first_name: str = models.CharField(max_length=150, blank=True)
    last_name: str = models.CharField(max_length=150, blank=True)
    email: str = models.EmailField(blank=True, unique=True)
    balance: int = models.DecimalField(decimal_places=3, max_digits=10, default=0)
    groups: datetime = models.ManyToManyField(
        Group,
        verbose_name=("groups"),
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )


class UserProfile(BaseModel):
    user: uuid.UUID = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    about: str = models.TextField(max_length=1000)


class UserProduct(BaseModel):
    user: uuid.UUID = models.ForeignKey("users.User", on_delete=models.PROTECT)
    user_product: Decimal = models.ForeignKey("stock_market.Product", on_delete=models.PROTECT)
    quantity: Decimal = models.DecimalField(max_digits=10, decimal_places=3)
    price: Decimal = models.DecimalField(max_digits=10, decimal_places=3)

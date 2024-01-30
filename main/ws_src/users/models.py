import uuid
from django.db import models

from ws_src.common.models import BaseModel
from ws_src.common.choices import BaseUserTypes
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(choices=BaseUserTypes.choices, max_length=20, default=BaseUserTypes.DEFAULT_USER)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, unique=True)
    balance = models.DecimalField(decimal_places=3, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
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

    def __str__(self):
        return f"username {self.username} | user id - {self.id}"


class UserProfile(BaseModel):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    about = models.TextField(max_length=1000)


class UserProduct(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    user_product = models.ForeignKey("stock_market.Product", on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f" user - {self.user_id} | product - {self.user_product_id}"

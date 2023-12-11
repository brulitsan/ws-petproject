import uuid

from django.db import models
from ws_src.common.choices import BaseUserTypes
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = (
        models.CharField(
            max_length=150,
            unique=True,
            help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        ),
    )
    role = models.CharField(choices=BaseUserTypes.choices, max_length=20)
    first_name = models.CharField(max_length=150, blank=True)
    user_balance = models.DecimalField(decimal_places=3, max_digits=3)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, unique=True)
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

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        help_text=("Specific permissions for this user."),
        related_name="custom_user_set",
        related_query_name="user",
    )
    access_token = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"username {self.username} | user id - {self.id}"


class UserProfile(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    about = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class UserProduct(models.Model):
    user_id: models.ForeignKey("users.User", on_delete=models.PROTECT)
    user_product_id = models.OneToOneField(
        "stock_market.Product", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" user - {self.user_id} | product - {self.user_product_id}"

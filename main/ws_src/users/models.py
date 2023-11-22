import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from main.ws_src.stock_market.models import Coin


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = (
        (1, "пользователь"),
        (2, "аналитик"),
        (3, "администратор"),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    role = models.CharField(choices=roles)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    id = models.OneToOneField(User.id, on_delete=models.CASCADE)
    about = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class UserCoin(models.Model):
    UserCoin_id = models.ForeignKey(Coin.id, on_delete=models.CASCADE)


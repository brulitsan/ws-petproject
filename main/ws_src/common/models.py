from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

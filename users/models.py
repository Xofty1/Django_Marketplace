from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    coins = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0)

from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User, Group, AbstractUser


class Seller(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


def product_image_upload_path(instance, filename):
    # Если ID еще нет, присвоим временное значение `unknown`
    product_id = instance.id if instance.id else 'unknown'
    return f'product_images/{product_id}/{filename}'

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True, default=None)


class UserStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name





class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

from django.contrib.auth.hashers import make_password
from django.db import models


class PickupPoint(models.Model):
    address = models.CharField(max_length=50)


class Seller(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=4)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=50)


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Courier(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)


class Order(models.Model):
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    delivery_type = models.CharField(max_length=20, choices=[
        ('pickup', 'Pickup'),
        ('courier', 'Courier'),
    ])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class CourierOrder(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

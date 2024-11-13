from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User

class PickupPoint(models.Model):
    address = models.CharField(max_length=50)


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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(
        upload_to='product_images/')  # Изображения будут храниться в media/product_images/

    def __str__(self):
        return f"Image for {self.product.name}"


class UserStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



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



class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.client.name}"

    def total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
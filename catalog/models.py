from django.db import models

from users.models import User

def product_image_upload_path(instance, filename):
    # Если ID еще нет, присвоим временное значение `unknown`
    product_id = instance.id if instance.id else 'unknown'
    return f'product_images/{product_id}/{filename}'

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True, default=None)


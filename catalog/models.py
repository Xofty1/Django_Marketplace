from django.db import models

from users.models import User


def product_image_upload_path(instance, filename):
    # Если ID еще нет, присвоим временное значение `unknown`
    product_id = instance.id if instance.id else 'unknown'
    return f'product_images/{product_id}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="products")
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="products")
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True,
                              null=True,
                              default="product_images/default_product.jpg")

    def save(self, *args, **kwargs):
        # Если изображение явно удалено (установлено None или ''), вернуть значение по умолчанию
        if not self.image:
            self.image = "product_images/default_product.jpg"
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удалить файл изображения перед удалением объекта
        if self.image and self.image.name != "product_images/default_product.jpg":
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
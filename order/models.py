from django.db import models

from catalog.models import Product
from users.models import User


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, blank=True, null=True,
        verbose_name="Пользователь", default=None
    )
    created_timestamp = models.DateTimeField(auto_now_add=True,
                                             verbose_name="Дата создания заказа")

    requires_delivery = models.BooleanField(default=False,
                                            verbose_name="Требуется доставка")
    delivery_address = models.TextField(null=True, blank=True,
                                        verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False,
                                         verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    total_cost = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0.00,
                                     verbose_name="Общая стоимость")
    # Статус заказа можно ограничить возможными значениями
    STATUS_CHOICES = [
        ('in_progress', 'В обработке'),
        ('paid', 'Оплачено'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='in_progress',
                              verbose_name="Статус заказа")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"

    def calculate_total_cost(self):
        total = sum(item.product.price * item.quantity for item in
                    self.orderitem_set.all())
        self.total_cost = total
        self.save()
        return self.total_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT,
                                null=True, verbose_name="Продукт",
                                default=None)
    quantity = models.PositiveIntegerField(default=0,
                                           verbose_name="Количество товара")
    created_timestamp = models.DateTimeField(auto_now_add=True,
                                             verbose_name="Дата продажи")

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    # Метод для вычисления стоимости товара в заказе
    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.product.name} | Заказ № {self.order.pk}"

class CourierOrder(models.Model):
    courier = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booked_orders",
        verbose_name="Курьер"
    )
    order = models.OneToOneField(
        'Order', on_delete=models.CASCADE, related_name="courier_booking",
        verbose_name="Заказ"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Курьер: {self.courier.username} - Заказ #{self.order.id}"
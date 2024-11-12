from django.contrib import admin
from .models import PickupPoint, Seller, Product, Client, Courier, Order, OrderProduct, CourierOrder

# Регистрируем каждую модель в админке
admin.site.register(PickupPoint)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Courier)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(CourierOrder)

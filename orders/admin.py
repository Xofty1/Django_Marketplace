from django.contrib import admin
from .models import Profile, UserStatus, PickupPoint, Seller, Product, Client, Courier, Order, OrderProduct, CourierOrder, ProductImage, Cart, CartItem

# Регистрируем каждую модель в админке
admin.site.register(PickupPoint)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Courier)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(CourierOrder)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Profile)
admin.site.register(UserStatus)

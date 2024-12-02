from django.contrib.auth.models import Group
from rest_framework import serializers

from cart.models import Cart
from catalog.models import Product, Category
from order.models import Order, OrderItem, CourierOrder
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'address', 'phone', 'coins']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'count', 'category', 'seller', 'image']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Поле user только для чтения

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_timestamp', 'requires_delivery', 'delivery_address', 'is_paid', 'total_cost', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'created_timestamp']

class CourierOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierOrder
        fields = ['id', 'courier', 'order']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
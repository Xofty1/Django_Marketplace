from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProductViewSet, CartViewSet, OrderViewSet, OrderItemViewSet,
    CourierOrderViewSet, CategoryViewSet, GroupViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'courier-orders', CourierOrderViewSet,
                basename='courier-order')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = router.urls

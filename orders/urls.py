from django.urls import path

from django.conf.urls.static import static
from marketplace import settings
from orders.views import register, login_view, home, logout_view, \
    product_detail, add_to_cart, remove_from_cart, cart_view, add_product

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart,
         name='remove_from_cart'),
    path('cart/', cart_view, name='cart'),
    path('add_product/', add_product, name='add_product'),
]

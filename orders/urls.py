from django.urls import path
from orders.views import register, login_view, home, logout_view, \
    product_detail, add_product

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
]

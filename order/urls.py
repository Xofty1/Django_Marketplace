from django.urls import path
from .views import order_create, order_detail, order_list, \
    order_list_for_courier, book_order

app_name = 'order'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('', order_list, name='order_list'),
    path('courier/', order_list_for_courier, name='order_list_for_courier'),
    path('<int:order_id>/', order_detail, name='order_detail'),
    path('book_order/<int:order_id>', book_order, name='book_order'),
]
from django.urls import path, reverse_lazy

from cart.views import cart_add, cart_remove, cart, cart_update

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('', cart, name='cart'),
    path('update/<int:product_id>/', cart_update,
         name='cart_update'),

]
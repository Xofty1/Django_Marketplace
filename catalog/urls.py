from django.urls import path, reverse_lazy

from catalog.views import catalog_view, product_detail, add_product

app_name = 'catalog'

urlpatterns = [

    path('<int:product_id>/', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
    path('', catalog_view, name='catalog'),
]

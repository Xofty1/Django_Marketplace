from django.urls import path, reverse_lazy

from catalog.views import catalog_view, product_detail, add_product, \
    seller_products, update_product, delete_product, add_random_product, \
    generate_graphs

app_name = 'catalog'

urlpatterns = [

    path('<int:product_id>/', product_detail, name='product_detail'),
    path('add_random/', add_random_product, name='add_random_product'),
    path('add/', add_product, name='add_product'),

    path('seller_products/', seller_products, name='seller_products'),
    path('', catalog_view, name='catalog'),
    path('update/<int:pk>/', update_product, name='update_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
    path('generate_graphs/', generate_graphs, name='generate_graphs'),
]

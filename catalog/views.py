from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from catalog.forms import AddProductForm
from catalog.models import Product


def catalog_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/catalog.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)


    return render(request, 'catalog/product_detail.html',
                  {'product': product} )

def is_seller(user):
    return user.groups.filter(name='Seller').exists()

def is_courier(user):
    return user.groups.filter(name='Courier').exists()
def is_seller(user):
    return user.groups.filter(name='Seller').exists()

@login_required
@user_passes_test(is_seller)
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            product.image = form.cleaned_data["image"]
            product.save()
            return redirect('catalog:catalog')
    else:
        form = AddProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})



@login_required
@user_passes_test(is_seller)
def manage_products(request):
    # Доступ для продавцов
    pass

@login_required
@user_passes_test(is_courier)
def manage_orders(request):
    # Доступ для курьеров
    pass
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
                  {'product': product})


def is_seller(user):
    return user.groups.filter(name='Seller').exists()


def is_courier(user):
    return user.groups.filter(name='Courier').exists()


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
def seller_products(request):
    # Получаем продукты, добавленные текущим пользователем
    products = Product.objects.filter(seller=request.user)

    return render(request, 'catalog/seller_products.html', {'products': products})




@login_required
@user_passes_test(is_seller)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:seller_products')
    else:
        form = AddProductForm(instance=product)

    return render(request, 'catalog/update_product.html', {'form': form, 'product': product})


@login_required
@user_passes_test(is_seller)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:seller_products')
    return render(request, 'catalog/delete_product.html', {'product': product})














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

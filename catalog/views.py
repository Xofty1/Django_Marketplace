import os
from decimal import Decimal

import matplotlib

matplotlib.use('Agg')
from django.db.models import Count
from faker import Faker

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect

from catalog.forms import AddProductForm
from catalog.models import Product, Category
import matplotlib.pyplot as plt
from django.shortcuts import render

faker = Faker()

from django.core.paginator import Paginator

def catalog_view(request):
    # Получение всех продуктов
    products = Product.objects.all().order_by('-id')

    # Фильтры по GET-параметрам
    category_ids = request.GET.getlist('category')  # Выбранные категории
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Применение фильтров
    if category_ids:
        products = products.filter(category__id__in=category_ids)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Пагинация
    paginator = Paginator(products, 20)  # 20 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передача категорий для фильтров
    categories = Category.objects.all()

    return render(
        request,
        'catalog/catalog.html',
        {
            'page_obj': page_obj,
            'categories': categories,
            'selected_categories': category_ids,  # Передача выбранных категорий
            'min_price': min_price,               # Передача фильтра цен
            'max_price': max_price                # Передача фильтра цен
        }
    )


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
def add_random_product(request):
    if request.method == 'POST':
        seller = request.user

        categories = list(Category.objects.all())

        if not categories:
            return render(request, 'catalog/seller_products.html', {
                'products': Product.objects.filter(seller=request.user)
            })

        for _ in range(50):
            Product.objects.create(
                seller=seller,
                count=faker.random_int(min=1, max=100),
                price=Decimal(faker.random_int(min=100, max=10000) / 100),
                category=faker.random.choice(categories),
                name=faker.word().capitalize(),
                description=faker.text(max_nb_chars=200)  # Добавляем описание
            )

        return redirect('catalog:seller_products')

    return redirect('users:coins_page')

@login_required
@user_passes_test(is_seller)

def seller_products(request):
    # Получение всех продуктов
    products = Product.objects.filter(seller=request.user).order_by('-id')

    # Фильтры по GET-параметрам
    category_ids = request.GET.getlist('category')  # Выбранные категории
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Применение фильтров
    if category_ids:
        products = products.filter(category__id__in=category_ids)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Пагинация
    paginator = Paginator(products, 20)  # 20 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передача категорий для фильтров
    categories = Category.objects.all()

    return render(
        request,
        'catalog/catalog.html',
        {
            'page_obj': page_obj,
            'categories': categories,
            'selected_categories': category_ids,  # Передача выбранных категорий
            'min_price': min_price,               # Передача фильтра цен
            'max_price': max_price,
            'seller_request': True
        }
    )





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
def generate_graphs(request):
    if request.method == 'POST':
        graph_dir = 'media/graphs'
        os.makedirs(graph_dir, exist_ok=True)

        # 1. Количество продуктов по категориям
        category_counts = Product.objects.values('category__name').annotate(count=Count('id'))
        categories = [item['category__name'] for item in category_counts]
        counts = [item['count'] for item in category_counts]

        plt.figure(figsize=(10, 6))
        plt.bar(categories, counts, color='skyblue')
        plt.title('Количество продуктов по категориям', fontsize=16)
        plt.xlabel('Категории', fontsize=12)
        plt.ylabel('Количество продуктов', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(graph_dir, 'category_counts.png'))
        plt.close()

        # 2. Распределение цен
        prices = [product.price for product in Product.objects.all()]

        plt.figure(figsize=(10, 6))
        plt.hist(prices, bins=20, color='green', edgecolor='black')
        plt.title('Распределение цен продуктов', fontsize=16)
        plt.xlabel('Цена', fontsize=12)
        plt.ylabel('Количество', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(graph_dir, 'price_distribution.png'))
        plt.close()

        # 3. Круговая диаграмма: Количество продуктов по продавцам
        seller_counts = Product.objects.values('seller__username').annotate(count=Count('id'))
        sellers = [item['seller__username'] for item in seller_counts]
        seller_counts = [item['count'] for item in seller_counts]

        plt.figure(figsize=(8, 8))
        plt.pie(seller_counts, labels=sellers, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Доля продуктов по продавцам', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(graph_dir, 'seller_distribution.png'))
        plt.close()

        # Передаем информацию о готовых графиках
        return render(request, 'catalog/generate_graphs.html', {'graphs': True})

    # Пустая форма, если метод GET
    return render(request, 'catalog/generate_graphs.html', {'graphs': False})
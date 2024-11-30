from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from cart.models import Cart
from catalog.models import Product

from django.http import JsonResponse
from django.views import View
from django.db import transaction
from .models import Product, Cart


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user,
                                                    product=product)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, 'Некорректное количество.')
            return redirect('catalog:product_detail', product_id=product.id)

        if quantity < 1:
            messages.error(request, 'Количество должно быть больше 0.')
            return redirect('catalog:product_detail', product_id=product.id)

        # Проверяем, достаточно ли товара на складе
        total_quantity = cart_item.quantity + quantity if not created else quantity
        if total_quantity > product.count:
            messages.error(
                request,
                f'Недостаточно товара "{product.name}" на складе. Доступно: {product.count}.'
            )
            return redirect('catalog:product_detail', product_id=product.id)

        # Обновляем количество в корзине
        if created:  # Если товар только добавляется
            cart_item.quantity = quantity
        else:  # Если товар уже есть, увеличиваем его количество
            cart_item.quantity += quantity

        cart_item.save()
        messages.success(request, f'{product.name} добавлен в корзину.')
        return redirect('cart:cart')

    return redirect('catalog:product_detail', product_id=product.id)


@login_required
def cart_remove(request, product_id):
    cart_item = Cart.objects.filter(user=request.user,
                                    product_id=product_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, 'Товар удалён из корзины.')
    return redirect('cart_detail')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'cart/cart_detail.html',
                  {'cart_items': cart_items})


@login_required
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(Cart, user=request.user, product=product)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            if product.count >= cart_item.quantity + 1:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request,
                                 f'Количество товара "{product.name}" увеличено.')
            else:
                messages.error(request,
                               f'Недостаточно товара "{product.name}" в наличии. Доступно: {product.count}.')
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request,
                                 f'Количество товара "{product.name}" уменьшено.')
            else:
                cart_item.delete()
                messages.success(request,
                                 f'Товар "{product.name}" удалён из корзины.')

    return redirect('cart:cart')  # Возвращаемся на страницу корзины


@login_required
def cart_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(Cart, user=request.user, product=product)

    if request.method == 'POST':
        cart_item.delete()
    return redirect('cart:cart')  # Возвращаемся на страницу корзины

from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from catalog.models import Product
from .forms import OrderForm
from .models import Order, OrderItem, CourierOrder
from cart.models import Cart


def is_courier(user):
    return user.groups.filter(name='Courier').exists()


@login_required
def order_create(request):
    # Получаем товары из корзины
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Ваша корзина пуста!")
        return redirect('cart:cart')  # Перенаправление обратно в корзину

    # Если запрос POST, то создаем заказ
    if request.method == 'POST':
        # Создаем заказ на основе формы
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Создаем заказ
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()  # Сохраняем заказ

            # Добавляем товары в заказ
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            order.calculate_total_cost()

            # Сравниваем стоимость с количеством монет пользователя
            if order.total_cost > request.user.coins:
                message = "У вас недостаточно средств для оформления заказа!"
                return render(request, 'users/coins_page.html',
                              {'message': message})

            # Вычитаем стоимость заказа из монет пользователя
            request.user.coins -= order.total_cost
            request.user.save()
            for cart_item in cart_items:
                try:
                    product = Product.objects.get(id=cart_item.product.id)
                    if product.count >= cart_item.quantity:
                        product.count -= cart_item.quantity
                        product.save()
                    else:
                        raise ValueError(
                            f"Недостаточно товара {product.name} на складе.")
                except Product.DoesNotExist:
                    raise ValueError(
                        f"Продукт с ID {cart_item.product.id} не найден.")
            # Очистить корзину после оформления
            cart_items.delete()

            return redirect('order:order_detail',
                            order_id=order.id)  # Перенаправляем на страницу заказа

    else:
        order_form = OrderForm()

    return render(request, 'order/order_create.html',
                  {'order_form': order_form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()  # Получаем все элементы заказа
    return render(request, 'order/order_detail.html',
                  {'order': order, 'order_items': order_items})


@login_required
def order_list(request):
    # Получаем все заказы текущего пользователя
    orders = Order.objects.filter(user=request.user).order_by(
        '-created_timestamp')
    return render(request, 'order/order_list.html', {'orders': orders})


@login_required
@user_passes_test(is_courier)
def order_list_for_courier(request):
    orders = Order.objects.all().order_by(
        '-created_timestamp')
    return render(request, 'order/order_for_courier.html',
                  {'orders': orders})


@login_required
def book_order(request, order_id):
    # Проверяем, является ли пользователь курьером
    if not request.user.groups.filter(name='Courier').exists():
        return HttpResponseForbidden(
            "Только курьеры могут бронировать заказы.")

    order = get_object_or_404(Order, id=order_id)

    # Проверяем, является ли заказ с доставкой
    if not order.requires_delivery:
        return HttpResponseForbidden(
            "Этот заказ не требует доставки и не может быть забронирован курьером.")

    # Проверяем, не забронирован ли заказ
    if hasattr(order, 'courier_booking'):
        return HttpResponseForbidden(
            "Этот заказ уже забронирован другим курьером.")

    order.status = "shipped"
    order.save()
    CourierOrder.objects.create(courier=request.user, order=order)

    return redirect(
        'order:order_list_for_courier')  # Перенаправление на список заказов

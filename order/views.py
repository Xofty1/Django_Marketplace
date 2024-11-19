from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import OrderForm
from .models import Order, OrderItem
from cart.models import Cart


@login_required
def create_order(request):
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
                messages.error(request,
                               "У вас недостаточно средств для оформления заказа!")
                return redirect('cart:cart')

            # Вычитаем стоимость заказа из монет пользователя
            request.user.coins -= order.total_cost
            request.user.save()

            # Очистить корзину после оформления
            cart_items.delete()

            messages.success(request, "Ваш заказ был успешно оформлен!")
            return redirect('order:order_detail',
                            order_id=order.id)  # Перенаправляем на страницу заказа

    else:
        order_form = OrderForm()

    return render(request, 'order/order_create.html',
                  {'order_form': order_form})

# @login_required
# def order_detail(request, order_id):
#     # Извлекаем заказ по его ID
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#
#     # Получаем список товаров в заказе
#     cart_items = order.cart_items.all()
#
#     # Передаем информацию о заказе и товарах в шаблон
#     return render(request, 'order/order_detail.html', {
#         'order': order,
#         'cart_items': cart_items,
#     })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()  # Получаем все элементы заказа
    return render(request, 'order/order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def order_list(request):
    # Получаем все заказы текущего пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_timestamp')
    return render(request, 'order/order_list.html', {'orders': orders})
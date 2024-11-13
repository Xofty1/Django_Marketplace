from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from marketplace.settings import MEDIA_ROOT
from .forms import ClientRegistrationForm, ClientLoginForm, AddProductForm, UserRegistrationForm
from .models import Product, Cart, CartItem, Profile
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

import os
from django.conf import settings

def home(request):
    products = Product.objects.all()
    return render(request, 'orders/home.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product_images = product.images.all()

    print(product.image.url)

    return render(request, 'orders/product_detail.html',
                  {'product': product, 'product_images': product_images})


# def register(request):
#     if request.method == 'POST':
#         form = ClientRegistrationForm(request.POST)
#         if form.is_valid():
#             client = form.save(commit=False)
#             client.set_password(form.cleaned_data['password'])
#             client.save()
#             return redirect('success')
#     else:
#         form = ClientRegistrationForm()
#     return render(request, 'orders/authenticate.html', {'form': form, 'form_type': 'register'})
#



# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             # Создаем пользователя с `User` моделью
#             user = User.objects.create_user(
#                 username=form.cleaned_data['email'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password'],
#             )
#             user.save()
#
#             # Создаем профиль пользователя
#             Profile.objects.create(user=user, status=form.cleaned_data.get('status', 1))  # где status — поле с уровнем доступа
#
#             login(request, user)
#             return redirect('success')
#     else:
#         form = ClientRegistrationForm()
#     return render(request, 'orders/authenticate.html', {'form': form, 'form_type': 'register'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user.save()

            # Назначаем пользователя в группу на основе выбора в форме
            role = form.cleaned_data.get('role')  # Пример: выбираем роль пользователя из формы
            group = Group.objects.get(name=role)
            user.groups.add(group)

            login(request, user)
            return redirect('success')
    else:
        form = UserRegistrationForm()
    return render(request, 'orders/authenticate.html', {'form': form, 'form_type': 'register'})


def login_view(request):
    if request.method == 'POST':
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            client = authenticate(request, email=email, password=password)

            if client is not None:
                login(request, client)
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = ClientLoginForm()

    return render(request, 'orders/authenticate.html', {'form': form, 'form_type': 'login'})


def logout_view(request):
    logout(request)
    return redirect('orders/login')


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', [])

    cart_item = next(
        (item for item in cart if item['product_id'] == product.id), None)

    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart.append({'product_id': product.id, 'quantity': 1})

    request.session['cart'] = cart
    return redirect('orders/cart')


def cart_view(request):
    cart = request.session.get('cart', [])
    return render(request, 'orders/cart/cart.html', {'cart': cart})



# @login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # cart, created = Cart.objects.get_or_create(user=request.client)

    # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # if not created:
    #     cart_item.quantity += 1
    #     cart_item.save()

    return redirect('orders/cart')

# @login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.client)
    return render(request, 'orders/cart/cart.html', {'cart': cart})


# @login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('orders/cart')


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        product = form.save(commit=False)
        product.save()
        if form.is_valid():
            product.image = form.cleaned_data["image"]
            product.save()
            return redirect('../home/')
    else:
        form = AddProductForm()

    return render(request, 'orders/add_product.html', {'form': form})


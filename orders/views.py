from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .forms import ClientLoginForm, AddProductForm, UserRegistrationForm
from .models import Product
from django.contrib.auth.models import User, Group


def home(request):
    products = Product.objects.all()
    return render(request, 'orders/home.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product_images = product.images.all()

    return render(request, 'orders/product_detail.html',
                  {'product': product, 'product_images': product_images})


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

            role = form.cleaned_data.get('role')
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


@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        product = form.save(commit=False)
        product.save()
        if form.is_valid():
            product.image = form.cleaned_data["image"]
            product.save()
            return redirect('catalog:catalog')
    else:
        form = AddProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ClientRegistrationForm, ClientLoginForm

def home(request):
    return HttpResponse("Home")

def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(form.cleaned_data['password'])
            client.save()
            return redirect('success')
    else:
        form = ClientRegistrationForm()
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
    return redirect('login')
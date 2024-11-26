from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import LoginView, PasswordChangeView, \
    PasswordResetConfirmView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from catalog.models import Product
from order.models import Order
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, \
    UserPasswordChangeForm, UserSetPasswordForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('catalog:catalog')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)
        user = form.instance

        # Назначаем группу "Client" по умолчанию
        client_group, _ = Group.objects.get_or_create(name='Client')
        user.groups.add(client_group)

        # Назначаем выбранную группу, если она указана
        selected_group_name = form.cleaned_data.get('group')
        if selected_group_name:
            selected_group, _ = Group.objects.get_or_create(name=selected_group_name)
            user.groups.add(selected_group)

        return response

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalog:catalog'))

def home_view(request):
    return HttpResponseRedirect(reverse('catalog:catalog'))

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"  # Укажите ваш шаблон
    form_class = UserSetPasswordForm  # Используйте вашу кастомную форму
    success_url = reverse_lazy("users:password_reset_complete")



def create_groups():
    # Создаем группы
    client_group, _ = Group.objects.get_or_create(name='Client')
    courier_group, _ = Group.objects.get_or_create(name='Courier')
    seller_group, _ = Group.objects.get_or_create(name='Seller')

    # Добавляем права для группы Seller
    product_ct = ContentType.objects.get_for_model(Product)
    add_product_permission = Permission.objects.get(codename='add_product', content_type=product_ct)
    seller_group.permissions.add(add_product_permission)

    # Добавляем права для группы Courier
    order_ct = ContentType.objects.get_for_model(Order)
    view_order_permission = Permission.objects.get(codename='view_order', content_type=order_ct)
    courier_group.permissions.add(view_order_permission)


@login_required
def increase_coins(request):
    user = request.user
    increase_amount = 10  # Увеличиваем на 10 монет

    # Увеличиваем количество монет
    user.coins += increase_amount
    user.save()

    # Добавляем сообщение об успехе
    messages.success(request, f'Вы получили {increase_amount} монет!')
    return render(request, 'users/coins_page.html', {'user': user})


@login_required
def coins_page(request):
    user = request.user
    return render(request, 'users/coins_page.html', {'user': user})
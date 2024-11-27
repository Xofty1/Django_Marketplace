from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    PasswordChangeForm, SetPasswordForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


# class RegisterUserForm(UserCreationForm):
#     username = forms.CharField(label="Логин")
#     password1 = forms.CharField(label="Пaрoль", widget=forms.PasswordInput())
#     password2 = forms.CharField(label="Повтор пароля",
#                                 widget=forms.PasswordInput())
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'first_name', 'last_name', 'password1',
#                   'password2']
#         labels = {
#             'email': 'E-mail',
#             'first_name': "Имя",
#             'last_name': "Фамилия"
#         }
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists():
#             raise forms.ValidationError("Тakoй E-mail yжe cyшествует!")
#         return email


class RegisterUserForm(UserCreationForm):
    GROUP_CHOICES = [
        ('Client', 'Клиент'),
        ('Courier', 'Курьер'),
        ('Seller', 'Продавец'),
    ]
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пaрoль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())
    group = forms.ChoiceField(label="Группа", choices=GROUP_CHOICES, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'address', 'phone', 'last_name', 'password1',
                  'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
            'address': "Адрес",
            'phone': "Телефон"
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Тakoй E-mail yжe cyшествует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин",widget=forms.TextInput(
        attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True,label="Почта",widget=forms.TextInput(
        attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
            'address': 'Адрес',
            'phone': "Телефон"
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput())


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}),
    )
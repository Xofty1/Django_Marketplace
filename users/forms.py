from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пaрoль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля",
                                widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1',
                  'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия"
        }

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if get_user_model().object.filter(email=email).exists():
    #         raise forms.ValidationError("Тakoй E-mail yжe cyшествует!")
    #     return email

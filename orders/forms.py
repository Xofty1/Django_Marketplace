from django import forms
from .models import Client, Product, UserStatus
from django.contrib.auth.models import User

#
# class UserRegistrationForm(forms.ModelForm):
#     status = forms.ModelChoiceField(queryset=UserStatus.objects.all(), required=True)
#     address = forms.CharField(max_length=255, required=False)
#     phone = forms.CharField(max_length=15, required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             Profile.objects.update_or_create(user=user, defaults={
#                 'status': self.cleaned_data['status'],
#                 'address': self.cleaned_data['address'],
#                 'phone': self.cleaned_data['phone']
#             })
#         return user


# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=[
        ('Client', 'Client'),
        ('Seller', 'Seller'),
        ('Courier', 'Courier'),
        ('Admin', 'Admin')
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # стандартные поля для UserCreationForm

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Сохраняем профиль с дополнительными данными
        profile = Profile(user=user, address=self.cleaned_data['address'], phone=self.cleaned_data['phone'], role=self.cleaned_data['role'])
        profile.save()

        return user



class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput,
                                       label="Confirm Password")

    class Meta:
        model = Client
        fields = ['name', 'address', 'email', 'phone', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        print(password)
        print(confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ClientLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['seller', 'count', 'price', 'category', 'name', 'image']

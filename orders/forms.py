from django import forms
from .models import Client


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

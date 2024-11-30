from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['requires_delivery', 'delivery_address']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Передаём пользователя в форму

    def clean_delivery_address(self):
        delivery_address = self.cleaned_data.get('delivery_address')

        if not delivery_address:
            raise forms.ValidationError(
                "Адрес доставки обязателен для заполнения.")

        return delivery_address


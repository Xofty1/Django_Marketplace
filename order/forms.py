from django import forms
from .models import Order

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['requires_delivery', 'delivery_address', 'payment_on_get']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['requires_delivery', 'delivery_address', 'payment_on_get']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Передаём пользователя в форму

    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get('requires_delivery')
        delivery_address = cleaned_data.get('delivery_address')

        if requires_delivery and not delivery_address:
            if self.user and self.user.address:
                cleaned_data['delivery_address'] = self.user.address
            else:
                raise forms.ValidationError("Адрес доставки обязателен для заполнения.")
        return cleaned_data

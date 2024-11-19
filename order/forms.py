from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['requires_delivery', 'delivery_address', 'payment_on_get']

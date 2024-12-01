from django.contrib.contenttypes import forms

from catalog.models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['count', 'price', 'category', 'name', 'description', 'image']
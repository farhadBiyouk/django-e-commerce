from django import forms
from cart.models import Cart, Compare


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity',)


class CompareForm(forms.ModelForm):
    class Meta:
        model = Compare
        fields = ('product',)

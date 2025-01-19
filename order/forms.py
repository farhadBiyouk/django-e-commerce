from django import forms
from order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'address']


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Code ...'}))
from django import forms
from .models import OrderItem, ShippingAddress

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'postal_code']

class AddProductToOrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


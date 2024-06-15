from django import forms
from .models import OrderItem, ShippingAddress, Product

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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),  # Добавление виджета для многострочного поля
            'price': forms.NumberInput(attrs={'step': '0.01'}),  # Добавление виджета для числового поля с шагом
            'stock': forms.NumberInput(attrs={'min': '0'}),  # Добавление виджета для числового поля с минимальным значением
        }

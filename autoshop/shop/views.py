from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Category, Product, Order, OrderItem, ShippingAddress
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product, Order, OrderItem, ShippingAddress
from .forms import OrderItemForm, ShippingAddressForm, AddProductToOrderForm

# Представление для отображения списка продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddProductToOrderForm()
        return context
    
def add_to_order(request, product_id):
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    form = AddProductToOrderForm(request.POST)

    if form.is_valid():
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += form.cleaned_data['quantity']
        order_item.save()
        return redirect('shop:order_detail', pk=order.id)
    
    return redirect('shop:product_list')

# Представление для отображения деталей продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

# Представление для создания заказа
class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'shop/create_order.html'
    fields = []

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:order_detail', kwargs={'pk': self.object.pk})

# Представление для добавления товара в заказ
class AddToOrderView(LoginRequiredMixin, CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'shop/add_to_order.html'

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['order_id'], customer=self.request.user.customer)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:order_detail', kwargs={'pk': self.object.order.pk})

# Представление для отображения деталей заказа
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'

# Представление для создания адреса доставки
class CreateShippingAddressView(LoginRequiredMixin, CreateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shop/create_shipping_address.html'

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['order_id'], customer=self.request.user.customer)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:order_detail', kwargs={'pk': self.object.order.pk})


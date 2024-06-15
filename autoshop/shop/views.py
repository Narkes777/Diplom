from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product, Order, OrderItem, ShippingAddress
from .forms import ShippingAddressForm, AddProductToOrderForm, ProductForm

# Представление для отображения списка продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddProductToOrderForm()
        return context
    
# Представление для добавления товара в заказ
def add_to_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = Order.objects.filter(customer=request.user.customer, complete=False).first()
    if not order:
        order = Order.objects.create(customer=request.user.customer)
    form = AddProductToOrderForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        if quantity <= 0:
            messages.error(request, "Invalid quantity.")
            return redirect('shop:product_list')
        
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += quantity
        order_item.save()

        messages.success(request, f"{quantity} {product.name}(s) added to your order.")
        return redirect('shop:order_detail', pk=order.id)
    
    return redirect('shop:product_list')


# Представление для создания продукта
class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('shop:product_list')

    def test_func(self):
        return self.request.user.is_staff

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
        form.instance.order = self.object.order
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shop:order_detail', kwargs={'pk': self.object.order.pk})


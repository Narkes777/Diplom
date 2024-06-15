from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import ProductListView, add_to_order, ProductDetailView, CreateOrderView, OrderDetailView, CreateShippingAddressView, ProductCreateView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('order/create/', CreateOrderView.as_view(), name='create_order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/add/<int:product_id>/', add_to_order, name='add_to_order'),
    path('order/<int:order_id>/shipping/', CreateShippingAddressView.as_view(), name='create_shipping_address'),
    path('login/', LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='shop:product_list'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

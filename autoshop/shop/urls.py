from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductListView, ProductDetailView, CreateOrderView, AddToOrderView, OrderDetailView, CreateShippingAddressView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('order/create/', CreateOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/add/', AddToOrderView.as_view(), name='add_to_order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:order_id>/shipping/', CreateShippingAddressView.as_view(), name='create_shipping_address'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

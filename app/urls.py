from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('orders/<int:order_id>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('products/review/', ProductReviewView.as_view(), name='product-review'),
]

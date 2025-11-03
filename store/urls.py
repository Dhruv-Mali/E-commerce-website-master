from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order-history'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('payments/cancelled/', views.cancelled, name='cancelled'),
]

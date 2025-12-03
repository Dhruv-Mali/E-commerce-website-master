from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('store/', views.store, name='store'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order-history'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('payment-cancelled/', views.payment_cancelled, name='payment-cancelled'),
    path('payment-success/', views.payment_success, name='payment-success'),
    
    # Custom Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-add-product/', views.admin_add_product, name='admin_add_product'),
    path('admin-edit-product/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin-delete-product/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
]

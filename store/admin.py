from django.contrib import admin
from .models import *

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user']
    search_fields = ['name', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'digital', 'in_stock']
    list_filter = ['category', 'digital']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'complete', 'transaction_id']
    list_filter = ['complete', 'date_ordered']
    search_fields = ['transaction_id', 'customer__name']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'date_added']
    list_filter = ['date_added']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'address', 'city', 'state', 'zipcode', 'date_added']
    list_filter = ['state', 'city']
    search_fields = ['address', 'city', 'state', 'zipcode']

# Import extended admin configurations
try:
    from .admin_extended import *
except ImportError:
    pass  # Extended admin not yet available
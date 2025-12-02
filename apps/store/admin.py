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
    list_display = ['id', 'customer', 'date_ordered', 'status', 'complete', 'transaction_id', 'get_cart_total']
    list_filter = ['complete', 'status', 'date_ordered']
    search_fields = ['transaction_id', 'customer__name']
    actions = ['confirm_order', 'mark_processing', 'mark_shipped', 'mark_delivered']
    
    def confirm_order(self, request, queryset):
        updated = queryset.update(complete=True, status='processing')
        self.message_user(request, f'{updated} order(s) confirmed and marked as processing.')
    confirm_order.short_description = 'Confirm selected orders'
    
    def mark_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} order(s) marked as processing.')
    mark_processing.short_description = 'Mark as Processing'
    
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')
    mark_shipped.short_description = 'Mark as Shipped'
    
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_delivered.short_description = 'Mark as Delivered'

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
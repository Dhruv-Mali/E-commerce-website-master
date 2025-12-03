from django.contrib import admin
from .models import Product, Customer, Order, OrderItem, ShippingAddress

# Customize admin site headers
admin.site.site_header = "Phone Store Admin"
admin.site.site_title = "Phone Store"
admin.site.index_title = "Welcome to Phone Store Administration"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user', 'get_total_orders']
    search_fields = ['name', 'email']
    list_filter = ['user__date_joined']
    readonly_fields = ['get_total_orders']
    list_per_page = 25
    
    def get_total_orders(self, obj):
        return obj.order_set.filter(complete=True).count()
    get_total_orders.short_description = 'Total Orders'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'digital', 'in_stock']
    list_filter = ['category', 'digital']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    readonly_fields = ['created_at', 'updated_at', 'views']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'digital')
        }),
        ('Category', {
            'fields': ('category',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    list_per_page = 20
    
    class Media:
        js = (
            'https://cdn.ckeditor.com/4.25.1-lts/standard/ckeditor.js',
            'admin/js/product_editor.js',
        )
        css = {
            'all': ('admin/css/product_admin.css',)
        }

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total']
    fields = ['product', 'quantity', 'get_total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'customer', 'date_ordered', 'status', 'complete', 'get_cart_total', 'payment_verified']
    list_filter = ['complete', 'status', 'date_ordered']
    search_fields = ['transaction_id', 'customer__name', 'customer__email']
    readonly_fields = ['date_ordered', 'get_cart_total', 'get_cart_items', 'transaction_id', 'stripe_payment_intent']
    inlines = [OrderItemInline]
    actions = ['mark_processing', 'mark_shipped', 'mark_delivered']
    fieldsets = (
        ('Order Details', {
            'fields': ('customer', 'complete', 'status')
        }),
        ('Payment Information', {
            'fields': ('transaction_id', 'stripe_payment_intent')
        }),
        ('Order Summary', {
            'fields': ('get_cart_total', 'get_cart_items', 'date_ordered'),
            'classes': ('collapse',)
        })
    )
    list_per_page = 25
    
    def get_queryset(self, request):
        # ONLY show completed orders with successful payment in admin
        qs = super().get_queryset(request)
        return qs.filter(complete=True, stripe_payment_intent__isnull=False)
    
    def payment_verified(self, obj):
        return obj.stripe_payment_intent is not None
    payment_verified.boolean = True
    payment_verified.short_description = 'Payment Verified'
    

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
    list_display = ['order', 'product', 'quantity', 'get_total', 'date_added']
    list_filter = ['date_added']
    readonly_fields = ['get_total', 'date_added']
    list_per_page = 30

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
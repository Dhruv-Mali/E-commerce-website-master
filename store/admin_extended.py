from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import Order, Product, OrderItem
from .models_extended import ProductReview, Coupon, ProductVariant, Newsletter

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    readonly_fields = ['created_at']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'discount_amount', 'active', 'valid_from', 'valid_to', 'used_count']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    list_editable = ['active']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'price_adjustment', 'stock']
    list_filter = ['name']
    search_fields = ['product__name', 'value']
    list_editable = ['stock', 'price_adjustment']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'active']
    list_filter = ['active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['active']

class SalesAnalyticsMixin:
    """Mixin for sales analytics"""
    
    def get_total_sales(self):
        return Order.objects.filter(complete=True).aggregate(
            total=Sum('orderitem__quantity')
        )['total'] or 0
    
    def get_revenue(self):
        orders = Order.objects.filter(complete=True)
        return sum(order.get_cart_total for order in orders)
    
    def get_top_products(self, limit=10):
        return Product.objects.annotate(
            total_sold=Sum('orderitem__quantity')
        ).order_by('-total_sold')[:limit]

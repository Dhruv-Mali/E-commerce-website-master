"""Admin configuration for extended models"""
from django.contrib import admin
from .models_extended import ProductReview, Wishlist, Coupon, RecentlyViewed, Newsletter

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'verified_purchase', 'created_at']
    list_filter = ['rating', 'verified_purchase', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']
    list_per_page = 25

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'valid_from', 'valid_to', 'active', 'used_count', 'max_uses']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    list_editable = ['active']
    list_per_page = 25

@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['viewed_at']
    list_per_page = 25

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'active']
    list_filter = ['active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['active']
    list_per_page = 25

"""Caching utilities for store app"""
from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # 15 minutes

# Track cached product keys so we can invalidate them
_product_cache_keys = set()

def get_cached_products(category=None, query=None):
    """Get cached product list"""
    cache_key = f'products_{category}_{query}'
    products = cache.get(cache_key)
    if products is None:
        from .models import Product
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        if query:
            products = products.filter(name__icontains=query)
        products = list(products.values())
        cache.set(cache_key, products, CACHE_TTL)
        _product_cache_keys.add(cache_key)
    return products

def invalidate_product_cache():
    """Clear product cache when products change.
    
    Uses tracked keys instead of delete_pattern() which is
    not supported by LocMemCache backend.
    """
    for key in list(_product_cache_keys):
        cache.delete(key)
    _product_cache_keys.clear()

def get_cart_count(user_id):
    """Get cached cart count"""
    cache_key = f'cart_count_{user_id}'
    return cache.get(cache_key, 0)

def set_cart_count(user_id, count):
    """Set cached cart count"""
    cache_key = f'cart_count_{user_id}'
    cache.set(cache_key, count, CACHE_TTL)

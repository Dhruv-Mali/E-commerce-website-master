from django.core.cache import cache
from django.conf import settings

def get_cached_products(category=None, timeout=300):
    """Cache products by category"""
    cache_key = f'products_{category or "all"}'
    products = cache.get(cache_key)
    
    if products is None:
        from .models import Product
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        products = list(products)
        cache.set(cache_key, products, timeout)
    
    return products

def invalidate_product_cache():
    """Invalidate all product caches"""
    from .models import Product
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    cache.delete('products_all')
    for category in categories:
        cache.delete(f'products_{category}')

def get_cached_cart(user_id, timeout=300):
    """Cache user cart"""
    cache_key = f'cart_{user_id}'
    return cache.get(cache_key)

def set_cached_cart(user_id, cart_data, timeout=300):
    """Set cached cart"""
    cache_key = f'cart_{user_id}'
    cache.set(cache_key, cart_data, timeout)

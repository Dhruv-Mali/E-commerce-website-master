from decimal import Decimal
from django.core.exceptions import ValidationError

def validate_order_total(submitted_total, calculated_total, tolerance=0.01):
    """Validate order total to prevent price manipulation"""
    if abs(float(submitted_total) - float(calculated_total)) > tolerance:
        raise ValidationError("Price mismatch detected")
    return True

def validate_stock_availability(product, quantity):
    """Validate product stock availability"""
    if not product.in_stock:
        raise ValidationError(f"{product.name} is out of stock")
    if product.stock < quantity:
        raise ValidationError(f"Only {product.stock} units available for {product.name}")
    return True

def sanitize_search_query(query):
    """Sanitize search input"""
    if not query:
        return ""
    return query.strip()[:100]

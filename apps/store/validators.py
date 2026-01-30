"""Validators for security and data integrity"""
from django.core.exceptions import ValidationError
import re

def validate_order_total(submitted, calculated, tolerance=0.01):
    """Validate order total matches calculated total"""
    if abs(float(submitted) - float(calculated)) > tolerance:
        raise ValidationError("Price mismatch detected. Please refresh and try again.")
    return True

def validate_stock_availability(product, quantity):
    """Validate product stock availability"""
    if not hasattr(product, 'stock'):
        return True
    if not product.in_stock or product.stock < quantity:
        raise ValidationError(f"Insufficient stock for {product.name}. Only {product.stock} available.")
    return True

def sanitize_search_query(query):
    """Sanitize search query to prevent injection"""
    if not query:
        return ""
    # Remove special characters except spaces and alphanumeric
    sanitized = re.sub(r'[^\w\s-]', '', query)
    return sanitized.strip()[:100]

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")
    return True

def validate_phone(phone):
    """Validate phone number"""
    pattern = r'^\+?1?\d{9,15}$'
    if not re.match(pattern, phone):
        raise ValidationError("Invalid phone number")
    return True

def validate_zipcode(zipcode):
    """Validate zipcode"""
    if not zipcode or len(zipcode) < 3:
        raise ValidationError("Invalid zipcode")
    return True

#!/usr/bin/env python
import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from apps.store.models import Product, Order, OrderItem, ShippingAddress

# Clear all fake data
print("Clearing all fake data...")

# Delete all products
Product.objects.all().delete()
print("[OK] Removed all products")

# Delete incomplete orders and their items
incomplete_orders = Order.objects.filter(complete=False)
OrderItem.objects.filter(order__in=incomplete_orders).delete()
incomplete_orders.delete()
print("[OK] Removed incomplete orders")

# Keep completed orders but remove their items if products don't exist
completed_orders = Order.objects.filter(complete=True)
for order in completed_orders:
    order.orderitem_set.filter(product__isnull=True).delete()

print("[OK] Cleaned up order items")
print("Database is now clean and ready for real products!")
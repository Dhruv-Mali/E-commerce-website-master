#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

count = Product.objects.count()
Product.objects.all().delete()
print(f"✅ Deleted {count} products")
print(f"Remaining products: {Product.objects.count()}")

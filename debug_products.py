#!/usr/bin/env python
import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from apps.store.models import Product

# Check products in database
products = Product.objects.all()
print(f"Total products in database: {products.count()}")

for product in products[:5]:  # Show first 5
    print(f"- {product.name} | Price: Rs.{product.price} | Stock: {product.stock}")

# Check if any products have issues
print(f"\nProducts with stock > 0: {Product.objects.filter(stock__gt=0).count()}")
print(f"Products with names: {Product.objects.exclude(name__isnull=True).exclude(name='').count()}")
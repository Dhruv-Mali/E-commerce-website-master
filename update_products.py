#!/usr/bin/env python
import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from apps.store.models import Product

# Remove all existing products
Product.objects.all().delete()
print("Removed all existing products")

# Add iPhone and Samsung phones
phones = [
    # iPhones
    {'name': 'iPhone 15 Pro Max', 'price': 134900, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system'},
    {'name': 'iPhone 15 Pro', 'price': 124900, 'digital': False, 'category': 'Smartphones', 'stock': 30, 'description': 'iPhone 15 Pro with A17 Pro chip and premium features'},
    {'name': 'iPhone 15', 'price': 79900, 'digital': False, 'category': 'Smartphones', 'stock': 40, 'description': 'iPhone 15 with Dynamic Island and improved cameras'},
    {'name': 'iPhone 14', 'price': 69900, 'digital': False, 'category': 'Smartphones', 'stock': 35, 'description': 'iPhone 14 with A15 Bionic chip and dual camera system'},
    {'name': 'iPhone 13', 'price': 59900, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'iPhone 13 with A15 Bionic and cinematic mode'},
    
    # Samsung Phones
    {'name': 'Samsung Galaxy S24 Ultra', 'price': 129999, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'Premium Samsung flagship with S Pen and AI features'},
    {'name': 'Samsung Galaxy S24+', 'price': 99999, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'Galaxy S24+ with enhanced display and camera'},
    {'name': 'Samsung Galaxy S24', 'price': 79999, 'digital': False, 'category': 'Smartphones', 'stock': 30, 'description': 'Latest Galaxy S24 with advanced AI capabilities'},
    {'name': 'Samsung Galaxy S23', 'price': 69999, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'Galaxy S23 with improved night photography'},
    {'name': 'Samsung Galaxy A54', 'price': 38999, 'digital': False, 'category': 'Smartphones', 'stock': 40, 'description': 'Mid-range Galaxy with great camera and battery life'},
]

for phone_data in phones:
    product = Product.objects.create(**phone_data)
    print(f"Added: {product.name} - Rs.{product.price}")

print(f"\nTotal products: {Product.objects.count()}")
print("Product update completed!")
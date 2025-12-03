#!/usr/bin/env python
import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from apps.store.models import Product

# Add more iPhone models
more_phones = [
    # More iPhones
    {'name': 'iPhone 15 Plus', 'price': 89900, 'digital': False, 'category': 'Smartphones', 'stock': 30, 'description': 'iPhone 15 Plus with larger display and all-day battery'},
    {'name': 'iPhone 14 Plus', 'price': 79900, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'iPhone 14 Plus with 6.7-inch display'},
    {'name': 'iPhone 12', 'price': 49900, 'digital': False, 'category': 'Smartphones', 'stock': 15, 'description': 'iPhone 12 with A14 Bionic and 5G capability'},
    {'name': 'iPhone SE (3rd Gen)', 'price': 43900, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'Compact iPhone with A15 Bionic chip'},
    
    # More Samsung Galaxy S Series
    {'name': 'Samsung Galaxy S23 Ultra', 'price': 124999, 'digital': False, 'category': 'Smartphones', 'stock': 18, 'description': 'Galaxy S23 Ultra with 200MP camera and S Pen'},
    {'name': 'Samsung Galaxy S23+', 'price': 94999, 'digital': False, 'category': 'Smartphones', 'stock': 22, 'description': 'Galaxy S23+ with enhanced performance'},
    {'name': 'Samsung Galaxy S22', 'price': 57999, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'Galaxy S22 with improved camera system'},
    
    # Samsung Galaxy A Series
    {'name': 'Samsung Galaxy A34', 'price': 30999, 'digital': False, 'category': 'Smartphones', 'stock': 35, 'description': 'Mid-range Galaxy with great value'},
    {'name': 'Samsung Galaxy A24', 'price': 23999, 'digital': False, 'category': 'Smartphones', 'stock': 40, 'description': 'Affordable Galaxy with solid performance'},
    {'name': 'Samsung Galaxy A14', 'price': 16999, 'digital': False, 'category': 'Smartphones', 'stock': 45, 'description': 'Budget-friendly Galaxy smartphone'},
    
    # Samsung Galaxy Note Series
    {'name': 'Samsung Galaxy Note 20 Ultra', 'price': 89999, 'digital': False, 'category': 'Smartphones', 'stock': 12, 'description': 'Premium Note with S Pen and productivity features'},
    
    # Samsung Galaxy Z Series (Foldables)
    {'name': 'Samsung Galaxy Z Fold5', 'price': 154999, 'digital': False, 'category': 'Smartphones', 'stock': 8, 'description': 'Revolutionary foldable smartphone'},
    {'name': 'Samsung Galaxy Z Flip5', 'price': 99999, 'digital': False, 'category': 'Smartphones', 'stock': 10, 'description': 'Compact flip phone with modern features'},
]

for phone_data in more_phones:
    product = Product.objects.create(**phone_data)
    print(f"Added: {product.name} - Rs.{product.price}")

print(f"\nTotal products now: {Product.objects.count()}")
print("Additional phones added successfully!")
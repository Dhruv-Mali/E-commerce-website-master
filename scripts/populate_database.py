#!/usr/bin/env python
"""
Consolidated script to populate database with sample products
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

PRODUCTS = [
    {'name': 'T-Shirt', 'price': 500, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Comfortable cotton t-shirt', 'image': 'images/tshirt.jpg'},
    {'name': 'Headphones', 'price': 2000, 'digital': False, 'category': 'Electronics', 'stock': 30, 'description': 'High-quality wireless headphones', 'image': 'images/headphone.jpg'},
    {'name': 'Watch', 'price': 1500, 'digital': False, 'category': 'Accessories', 'stock': 25, 'description': 'Stylish analog watch', 'image': 'images/watch.jpg'},
    {'name': 'Shoes', 'price': 3000, 'digital': False, 'category': 'Footwear', 'stock': 40, 'description': 'Premium running shoes', 'image': 'images/shoe.jpg'},
    {'name': 'Book', 'price': 300, 'digital': True, 'category': 'Books', 'stock': 100, 'description': 'Digital programming book', 'image': 'images/book.jpg'},
    {'name': 'Source Code', 'price': 1000, 'digital': True, 'category': 'Digital', 'stock': 100, 'description': 'Complete source code package', 'image': 'images/source_code.jpg'},
]

def populate():
    for data in PRODUCTS:
        product, created = Product.objects.get_or_create(name=data['name'], defaults=data)
        print(f"{'Created' if created else 'Exists'}: {product.name}")
    print(f"\nTotal products: {Product.objects.count()}")

if __name__ == '__main__':
    populate()

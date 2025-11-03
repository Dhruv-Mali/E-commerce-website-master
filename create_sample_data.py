#!/usr/bin/env python
"""
Script to create sample products for the e-commerce store
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

# Sample products data
products_data = [
    {'name': 'T-Shirt', 'price': 500, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Comfortable cotton t-shirt'},
    {'name': 'Headphones', 'price': 2000, 'digital': False, 'category': 'Electronics', 'stock': 30, 'description': 'High-quality wireless headphones'},
    {'name': 'Watch', 'price': 1500, 'digital': False, 'category': 'Accessories', 'stock': 25, 'description': 'Stylish analog watch'},
    {'name': 'Shoes', 'price': 3000, 'digital': False, 'category': 'Footwear', 'stock': 40, 'description': 'Premium running shoes'},
    {'name': 'Book', 'price': 300, 'digital': True, 'category': 'Books', 'stock': 100, 'description': 'Digital programming book'},
    {'name': 'Source Code', 'price': 1000, 'digital': True, 'category': 'Digital', 'stock': 100, 'description': 'Complete source code package'},
]

def create_sample_products():
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'price': product_data['price'],
                'digital': product_data['digital'],
                'category': product_data.get('category', ''),
                'stock': product_data.get('stock', 100),
                'description': product_data.get('description', '')
            }
        )
        if created:
            print(f"Created product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")

if __name__ == '__main__':
    create_sample_products()
    print("Sample data creation completed!")
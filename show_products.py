#!/usr/bin/env python
"""
Script to display all products with their details
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

def show_all_products():
    """Display all products with their details"""
    products = Product.objects.all().order_by('category', 'name')
    
    print("=" * 80)
    print("ALL PRODUCTS IN YOUR E-COMMERCE STORE")
    print("=" * 80)
    
    current_category = ""
    for product in products:
        if product.category != current_category:
            current_category = product.category
            print(f"\n[{current_category.upper() or 'UNCATEGORIZED'}]")
            print("-" * 40)
        
        print(f"  • {product.name}")
        print(f"    Price: Rs.{product.price}")
        print(f"    Stock: {product.stock}")
        print(f"    Type: {'Digital' if product.digital else 'Physical'}")
        print(f"    Image: {product.image or 'No image'}")
        print(f"    Description: {product.description}")
        print()
    
    print(f"Total Products: {products.count()}")
    print("=" * 80)

if __name__ == '__main__':
    show_all_products()
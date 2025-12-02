#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

def add_product():
    name = input("Product Name: ")
    price = int(input("Price: "))
    category = input("Category: ")
    stock = int(input("Stock: "))
    description = input("Description: ")
    digital = input("Digital? (yes/no): ").lower() == 'yes'
    image = input("Image path (e.g., images/product.jpg): ")
    
    product = Product.objects.create(
        name=name,
        price=price,
        category=category,
        stock=stock,
        description=description,
        digital=digital,
        image=image
    )
    print(f"\n✅ Product '{product.name}' added successfully!")
    print(f"Total products: {Product.objects.count()}")

if __name__ == '__main__':
    add_product()

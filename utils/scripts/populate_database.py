#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to populate database with products matching available images
"""
import os
import sys
import django
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

PRODUCTS = [
    # Electronics
    {'name': 'Wireless Headphones', 'price': 2499, 'digital': False, 'category': 'Electronics', 'stock': 45, 'description': 'Premium wireless headphones with noise cancellation', 'image': 'images/headphone.jpg'},
    {'name': 'Smartwatch', 'price': 3999, 'digital': False, 'category': 'Electronics', 'stock': 30, 'description': 'Fitness tracking smartwatch with heart rate monitor', 'image': 'images/watch.jpg'},
    {'name': 'Bluetooth Speaker', 'price': 1899, 'digital': False, 'category': 'Electronics', 'stock': 50, 'description': 'Portable wireless speaker with rich bass', 'image': 'images/bluetooth_speaker.jpg'},
    {'name': 'Laptop', 'price': 54999, 'digital': False, 'category': 'Electronics', 'stock': 15, 'description': 'High-performance laptop for work and gaming', 'image': 'images/laptop.jpg'},
    {'name': 'Smartphone', 'price': 29999, 'digital': False, 'category': 'Electronics', 'stock': 25, 'description': 'Latest smartphone with advanced camera system', 'image': 'images/smartphone.jpg'},
    {'name': 'Wireless Mouse', 'price': 799, 'digital': False, 'category': 'Electronics', 'stock': 60, 'description': 'Ergonomic wireless mouse with precision tracking', 'image': 'images/wireless_mouse.jpg'},
    {'name': 'Fitness Tracker', 'price': 2499, 'digital': False, 'category': 'Electronics', 'stock': 40, 'description': 'Smart fitness band with activity tracking', 'image': 'images/fitness_tracker.jpg'},
    
    # Clothing & Fashion
    {'name': 'Cotton T-Shirt', 'price': 599, 'digital': False, 'category': 'Clothing', 'stock': 100, 'description': 'Comfortable cotton t-shirt for everyday wear', 'image': 'images/tshirt.jpg'},
    {'name': 'Denim Jeans', 'price': 1499, 'digital': False, 'category': 'Clothing', 'stock': 75, 'description': 'Classic fit denim jeans with premium fabric', 'image': 'images/jeans.jpg'},
    {'name': 'Hoodie', 'price': 1899, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Warm and cozy hoodie for winter', 'image': 'images/hoodie.jpg'},
    
    # Footwear
    {'name': 'Running Shoes', 'price': 3499, 'digital': False, 'category': 'Footwear', 'stock': 40, 'description': 'Lightweight running shoes with cushioned sole', 'image': 'images/shoe.jpg'},
    {'name': 'Sneakers', 'price': 2999, 'digital': False, 'category': 'Footwear', 'stock': 55, 'description': 'Trendy sneakers for casual wear', 'image': 'images/sneakers.jpg'},
    
    # Accessories
    {'name': 'Sunglasses', 'price': 1299, 'digital': False, 'category': 'Accessories', 'stock': 70, 'description': 'UV protection sunglasses with stylish design', 'image': 'images/sunglasses.jpg'},
    {'name': 'Travel Backpack', 'price': 1999, 'digital': False, 'category': 'Accessories', 'stock': 35, 'description': 'Durable backpack with multiple compartments', 'image': 'images/backpack.jpg'},
    
    # Home & Kitchen
    {'name': 'Coffee Mug', 'price': 299, 'digital': False, 'category': 'Home & Kitchen', 'stock': 100, 'description': 'Ceramic coffee mug with elegant design', 'image': 'images/coffee_mug.jpg'},
    {'name': 'Desk Lamp', 'price': 1499, 'digital': False, 'category': 'Home & Kitchen', 'stock': 45, 'description': 'LED desk lamp with adjustable brightness', 'image': 'images/desk_lamp.jpg'},
    {'name': 'Plant Pot', 'price': 399, 'digital': False, 'category': 'Home & Kitchen', 'stock': 80, 'description': 'Modern ceramic pot for indoor plants', 'image': 'images/plant_pot.jpg'},
    
    # Furniture
    {'name': 'Gaming Chair', 'price': 12999, 'digital': False, 'category': 'Furniture', 'stock': 20, 'description': 'Ergonomic gaming chair with lumbar support', 'image': 'images/gaming_chair.jpg'},
    
    # Books & Digital
    {'name': 'Programming Book', 'price': 499, 'digital': True, 'category': 'Books', 'stock': 999, 'description': 'Complete guide to modern programming', 'image': 'images/book.jpg'},
    {'name': 'Source Code Package', 'price': 1999, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'Premium source code templates and projects', 'image': 'images/source_code.jpg'},
]

def populate():
    Product.objects.all().delete()
    print("Cleared existing products\n")
    
    for data in PRODUCTS:
        product = Product.objects.create(**data)
        print(f"[+] Created: {product.name} - Rs.{product.price}")
    
    print(f"\n[SUCCESS] Total products: {Product.objects.count()}")
    print(f"[INFO] Categories: {', '.join(Product.objects.values_list('category', flat=True).distinct())}")

if __name__ == '__main__':
    populate()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to populate database with products matching available images
"""
import os
import sys
import django
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
os.chdir(project_root)

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from apps.store.models import Product

PRODUCTS = [
    # iPhone Models
    {'name': 'iPhone 15 Pro Max', 'price': 134900, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system'},
    {'name': 'iPhone 15 Pro', 'price': 124900, 'digital': False, 'category': 'Smartphones', 'stock': 30, 'description': 'iPhone 15 Pro with A17 Pro chip and premium features'},
    {'name': 'iPhone 15 Plus', 'price': 89900, 'digital': False, 'category': 'Smartphones', 'stock': 30, 'description': 'iPhone 15 Plus with larger display and all-day battery'},
    {'name': 'iPhone 15', 'price': 79900, 'digital': False, 'category': 'Smartphones', 'stock': 40, 'description': 'iPhone 15 with Dynamic Island and improved cameras'},
    {'name': 'iPhone 14 Plus', 'price': 79900, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'iPhone 14 Plus with 6.7-inch display'},
    {'name': 'iPhone 14', 'price': 69900, 'digital': False, 'category': 'Smartphones', 'stock': 35, 'description': 'iPhone 14 with A15 Bionic chip and dual camera system'},
    {'name': 'iPhone 13', 'price': 59900, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'iPhone 13 with A15 Bionic and cinematic mode'},
    {'name': 'iPhone 12', 'price': 49900, 'digital': False, 'category': 'Smartphones', 'stock': 15, 'description': 'iPhone 12 with A14 Bionic and 5G capability'},
    {'name': 'iPhone SE (3rd Gen)', 'price': 43900, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'Compact iPhone with A15 Bionic chip'},
    
    # Samsung Galaxy Z Series (Foldables)
    {'name': 'Samsung Galaxy Z Fold5', 'price': 154999, 'digital': False, 'category': 'Smartphones', 'stock': 8, 'description': 'Revolutionary foldable smartphone'},
    {'name': 'Samsung Galaxy Z Flip5', 'price': 99999, 'digital': False, 'category': 'Smartphones', 'stock': 10, 'description': 'Compact flip phone with modern features'},
    
    # Samsung Galaxy S Series
    {'name': 'Samsung Galaxy S24 Ultra', 'price': 129999, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'Premium Samsung flagship with S Pen and AI features'},
    {'name': 'Samsung Galaxy S23 Ultra', 'price': 124999, 'digital': False, 'category': 'Smartphones', 'stock': 18, 'description': 'Galaxy S23 Ultra with 200MP camera and S Pen'},
    {'name': 'Samsung Galaxy S24+', 'price': 99999, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'Galaxy S24+ with enhanced display and camera'},
    {'name': 'Samsung Galaxy S23+', 'price': 94999, 'digital': False, 'category': 'Smartphones', 'stock': 22, 'description': 'Galaxy S23+ with enhanced performance'},
    {'name': 'Samsung Galaxy S24', 'price': 79999, 'digital': False, 'category': 'Smartphones', 'stock': 30, 'description': 'Latest Galaxy S24 with advanced AI capabilities'},
    {'name': 'Samsung Galaxy S23', 'price': 69999, 'digital': False, 'category': 'Smartphones', 'stock': 25, 'description': 'Galaxy S23 with improved night photography'},
    {'name': 'Samsung Galaxy S22', 'price': 57999, 'digital': False, 'category': 'Smartphones', 'stock': 20, 'description': 'Galaxy S22 with improved camera system'},
    
    # Samsung Galaxy Note Series
    {'name': 'Samsung Galaxy Note 20 Ultra', 'price': 89999, 'digital': False, 'category': 'Smartphones', 'stock': 12, 'description': 'Premium Note with S Pen and productivity features'},
    
    # Samsung Galaxy A Series
    {'name': 'Samsung Galaxy A54', 'price': 38999, 'digital': False, 'category': 'Smartphones', 'stock': 40, 'description': 'Mid-range Galaxy with great camera and battery life'},
    {'name': 'Samsung Galaxy A34', 'price': 30999, 'digital': False, 'category': 'Smartphones', 'stock': 35, 'description': 'Mid-range Galaxy with great value'},
    {'name': 'Samsung Galaxy A24', 'price': 23999, 'digital': False, 'category': 'Smartphones', 'stock': 40, 'description': 'Affordable Galaxy with solid performance'},
    {'name': 'Samsung Galaxy A14', 'price': 16999, 'digital': False, 'category': 'Smartphones', 'stock': 45, 'description': 'Budget-friendly Galaxy smartphone'},
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

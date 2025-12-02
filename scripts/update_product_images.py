#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

IMAGE_MAP = {
    'Wireless Headphones': 'images/headphone.jpg',
    'Smartwatch': 'images/watch.jpg',
    'Bluetooth Speaker': 'images/bluetooth_speaker.jpg',
    'Laptop': 'images/laptop.jpg',
    'Smartphone': 'images/smartphone.jpg',
    'Wireless Mouse': 'images/wireless_mouse.jpg',
    'Fitness Tracker': 'images/fitness_tracker.jpg',
    'Cotton T-Shirt': 'images/tshirt.jpg',
    'Denim Jeans': 'images/jeans.jpg',
    'Hoodie': 'images/hoodie.jpg',
    'Running Shoes': 'images/shoe.jpg',
    'Sneakers': 'images/sneakers.jpg',
    'Sunglasses': 'images/sunglasses.jpg',
    'Travel Backpack': 'images/backpack.jpg',
    'Coffee Mug': 'images/coffee_mug.jpg',
    'Plant Pot': 'images/plant_pot.jpg',
    'Gaming Chair': 'images/gaming_chair.jpg',
    'Programming Book': 'images/book.jpg',
    'Source Code Package': 'images/source_code.jpg',
}

def update_images():
    for name, image in IMAGE_MAP.items():
        try:
            product = Product.objects.get(name=name)
            product.image = image
            product.save()
            print(f"[+] Updated: {name}")
        except Product.DoesNotExist:
            print(f"[-] Not found: {name}")
    
    print(f"\n[SUCCESS] Updated {Product.objects.exclude(image='').count()} products")

if __name__ == '__main__':
    update_images()

#!/usr/bin/env python
"""
Script to fix missing images and add more products
"""
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

# Fix missing images and add more products
ADDITIONAL_PRODUCTS = [
    {
        'name': 'Coffee Mug',
        'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&h=500&fit=crop'
    },
    {
        'name': 'Gaming Chair',
        'price': 8000,
        'digital': False,
        'category': 'Furniture',
        'stock': 10,
        'description': 'Ergonomic gaming chair with lumbar support',
        'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop'
    },
    {
        'name': 'Bluetooth Speaker',
        'price': 1200,
        'digital': False,
        'category': 'Electronics',
        'stock': 25,
        'description': 'Portable wireless speaker with rich sound',
        'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&h=500&fit=crop'
    },
    {
        'name': 'Fitness Tracker',
        'price': 3500,
        'digital': False,
        'category': 'Electronics',
        'stock': 30,
        'description': 'Smart fitness tracker with heart rate monitor',
        'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500&h=500&fit=crop'
    },
    {
        'name': 'Desk Lamp',
        'price': 1800,
        'digital': False,
        'category': 'Home',
        'stock': 20,
        'description': 'Modern LED desk lamp with adjustable brightness',
        'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop'
    }
]

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filepath = os.path.join('static', 'images', filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def fix_and_add_products():
    """Fix missing images and add new products"""
    for product_data in ADDITIONAL_PRODUCTS:
        try:
            # Check if product exists (for Coffee Mug fix)
            try:
                product = Product.objects.get(name=product_data['name'])
                print(f"Updating existing product: {product_data['name']}")
            except Product.DoesNotExist:
                # Create new product
                product = Product.objects.create(
                    name=product_data['name'],
                    price=product_data.get('price', 0),
                    digital=product_data.get('digital', False),
                    category=product_data.get('category', ''),
                    stock=product_data.get('stock', 100),
                    description=product_data.get('description', '')
                )
                print(f"Created new product: {product_data['name']}")
            
            # Generate filename
            filename = f"{product_data['name'].lower().replace(' ', '_')}.jpg"
            
            # Download image
            if download_image(product_data['image_url'], filename):
                product.image = f"images/{filename}"
                product.save()
                print(f"Updated {product_data['name']} with image")
            
        except Exception as e:
            print(f"Error processing {product_data['name']}: {e}")

if __name__ == '__main__':
    print("Fixing missing images and adding more products...")
    fix_and_add_products()
    print("Process completed!")
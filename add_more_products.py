#!/usr/bin/env python
"""
Script to add more products with realistic images
"""
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

# Extended product catalog with realistic images
EXTENDED_PRODUCTS = [
    # Electronics
    {
        'name': 'Smartphone',
        'price': 25000,
        'digital': False,
        'category': 'Electronics',
        'stock': 20,
        'description': 'Latest Android smartphone with 128GB storage',
        'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&h=500&fit=crop'
    },
    {
        'name': 'Laptop',
        'price': 45000,
        'digital': False,
        'category': 'Electronics',
        'stock': 15,
        'description': 'High-performance laptop for work and gaming',
        'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&h=500&fit=crop'
    },
    {
        'name': 'Wireless Mouse',
        'price': 800,
        'digital': False,
        'category': 'Electronics',
        'stock': 50,
        'description': 'Ergonomic wireless mouse with precision tracking',
        'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&h=500&fit=crop'
    },
    
    # Clothing
    {
        'name': 'Jeans',
        'price': 1200,
        'digital': False,
        'category': 'Clothing',
        'stock': 35,
        'description': 'Premium denim jeans with perfect fit',
        'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&h=500&fit=crop'
    },
    {
        'name': 'Hoodie',
        'price': 1800,
        'digital': False,
        'category': 'Clothing',
        'stock': 25,
        'description': 'Comfortable cotton hoodie for casual wear',
        'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&h=500&fit=crop'
    },
    {
        'name': 'Sneakers',
        'price': 2500,
        'digital': False,
        'category': 'Footwear',
        'stock': 30,
        'description': 'Trendy sneakers for everyday comfort',
        'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop'
    },
    
    # Accessories
    {
        'name': 'Sunglasses',
        'price': 900,
        'digital': False,
        'category': 'Accessories',
        'stock': 40,
        'description': 'Stylish UV protection sunglasses',
        'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&h=500&fit=crop'
    },
    {
        'name': 'Backpack',
        'price': 1500,
        'digital': False,
        'category': 'Accessories',
        'stock': 20,
        'description': 'Durable travel backpack with multiple compartments',
        'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop'
    },
    
    # Home & Kitchen
    {
        'name': 'Coffee Mug',
        'price': 300,
        'digital': False,
        'category': 'Home',
        'stock': 60,
        'description': 'Ceramic coffee mug with elegant design',
        'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=500&h=500&fit=crop'
    },
    {
        'name': 'Plant Pot',
        'price': 450,
        'digital': False,
        'category': 'Home',
        'stock': 35,
        'description': 'Modern ceramic plant pot for indoor plants',
        'image_url': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500&h=500&fit=crop'
    },
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

def add_products_with_images():
    """Add new products with downloaded images"""
    for product_data in EXTENDED_PRODUCTS:
        try:
            # Check if product already exists
            if Product.objects.filter(name=product_data['name']).exists():
                print(f"Product '{product_data['name']}' already exists")
                continue
            
            # Generate filename
            filename = f"{product_data['name'].lower().replace(' ', '_')}.jpg"
            
            # Download image
            if download_image(product_data['image_url'], filename):
                # Create product
                product = Product.objects.create(
                    name=product_data['name'],
                    price=product_data['price'],
                    digital=product_data['digital'],
                    category=product_data['category'],
                    stock=product_data['stock'],
                    description=product_data['description'],
                    image=f"images/{filename}"
                )
                print(f"Created product: {product.name}")
            else:
                # Create product without image
                product = Product.objects.create(
                    name=product_data['name'],
                    price=product_data['price'],
                    digital=product_data['digital'],
                    category=product_data['category'],
                    stock=product_data['stock'],
                    description=product_data['description']
                )
                print(f"Created product without image: {product.name}")
                
        except Exception as e:
            print(f"Error creating {product_data['name']}: {e}")

if __name__ == '__main__':
    print("Adding new products with realistic images...")
    add_products_with_images()
    print("Product addition completed!")
#!/usr/bin/env python
"""
Script to download realistic product images and update the database
"""
import os
import django
import requests
from urllib.parse import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

# High-quality product images from Unsplash (free to use)
PRODUCT_IMAGES = {
    'T-Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop',
    'Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop',
    'Watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop',
    'Shoes': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop',
    'Book': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500&h=500&fit=crop',
    'Source Code': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500&h=500&fit=crop',
}

def download_image(url, filename):
    """Download image from URL and save to static/images/"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filepath = os.path.join('static', 'images', filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def update_product_images():
    """Update products with new image filenames"""
    for product_name, image_url in PRODUCT_IMAGES.items():
        try:
            product = Product.objects.get(name=product_name)
            
            # Generate filename
            filename = f"{product_name.lower().replace(' ', '_')}_new.jpg"
            
            # Download image
            if download_image(image_url, filename):
                # Update product image field
                product.image = f"images/{filename}"
                product.save()
                print(f"Updated {product_name} with new image")
            
        except Product.DoesNotExist:
            print(f"Product '{product_name}' not found")
        except Exception as e:
            print(f"Error updating {product_name}: {e}")

if __name__ == '__main__':
    print("Downloading realistic product images...")
    update_product_images()
    print("Image update completed!")
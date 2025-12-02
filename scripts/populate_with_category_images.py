#!/usr/bin/env python
import os, sys, django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

PRODUCTS = [
    # Electronics
    {'name': 'Wireless Headphones', 'price': 2499, 'digital': False, 'category': 'Electronics', 'stock': 45, 'description': 'Premium wireless headphones with noise cancellation', 'image': 'Electronics.jpg'},
    {'name': 'Smartwatch Pro', 'price': 3999, 'digital': False, 'category': 'Electronics', 'stock': 30, 'description': 'Fitness tracking smartwatch with heart rate monitor', 'image': 'Electronics (2).jpg'},
    {'name': 'Bluetooth Speaker', 'price': 1899, 'digital': False, 'category': 'Electronics', 'stock': 50, 'description': 'Portable wireless speaker with rich bass', 'image': 'Electronics (3).jpg'},
    {'name': 'Gaming Laptop', 'price': 54999, 'digital': False, 'category': 'Electronics', 'stock': 15, 'description': 'High-performance laptop for work and gaming', 'image': 'Electronics (4).jpg'},
    {'name': 'Smartphone 5G', 'price': 29999, 'digital': False, 'category': 'Electronics', 'stock': 25, 'description': 'Latest smartphone with advanced camera system', 'image': 'Electronics (5).jpg'},
    {'name': 'Wireless Mouse', 'price': 799, 'digital': False, 'category': 'Electronics', 'stock': 60, 'description': 'Ergonomic wireless mouse with precision tracking', 'image': 'Electronics (6).jpg'},
    {'name': 'Tablet Pro', 'price': 24999, 'digital': False, 'category': 'Electronics', 'stock': 40, 'description': 'Powerful tablet for productivity and entertainment', 'image': 'Electronics (7).jpg'},
    {'name': 'Smart TV 4K', 'price': 39999, 'digital': False, 'category': 'Electronics', 'stock': 20, 'description': 'Ultra HD smart TV with streaming apps', 'image': 'Electronics (8).jpg'},
    
    # Clothing
    {'name': 'Cotton T-Shirt', 'price': 599, 'digital': False, 'category': 'Clothing', 'stock': 100, 'description': 'Comfortable cotton t-shirt for everyday wear', 'image': 'Clothing.jpg'},
    {'name': 'Denim Jeans', 'price': 1499, 'digital': False, 'category': 'Clothing', 'stock': 75, 'description': 'Classic fit denim jeans with premium fabric', 'image': 'Clothing (2).jpg'},
    {'name': 'Hoodie', 'price': 1899, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Warm and cozy hoodie for winter', 'image': 'Clothing (3).jpg'},
    {'name': 'Formal Shirt', 'price': 1299, 'digital': False, 'category': 'Clothing', 'stock': 60, 'description': 'Professional formal shirt for office wear', 'image': 'Clothing (4).jpg'},
    {'name': 'Casual Jacket', 'price': 2499, 'digital': False, 'category': 'Clothing', 'stock': 40, 'description': 'Stylish casual jacket for all seasons', 'image': 'Clothing (5).jpg'},
    {'name': 'Sports Jersey', 'price': 899, 'digital': False, 'category': 'Clothing', 'stock': 80, 'description': 'Breathable sports jersey for active lifestyle', 'image': 'Clothing (6).jpg'},
    {'name': 'Winter Coat', 'price': 3499, 'digital': False, 'category': 'Clothing', 'stock': 30, 'description': 'Warm winter coat with insulation', 'image': 'Clothing (7).jpg'},
    {'name': 'Polo Shirt', 'price': 799, 'digital': False, 'category': 'Clothing', 'stock': 70, 'description': 'Classic polo shirt for casual occasions', 'image': 'Clothing (8).jpg'},
    {'name': 'Track Pants', 'price': 999, 'digital': False, 'category': 'Clothing', 'stock': 65, 'description': 'Comfortable track pants for gym and home', 'image': 'Clothing (9).jpg'},
    
    # Footwear
    {'name': 'Running Shoes', 'price': 3499, 'digital': False, 'category': 'Footwear', 'stock': 40, 'description': 'Lightweight running shoes with cushioned sole', 'image': 'Footwear.jpg'},
    {'name': 'Casual Sneakers', 'price': 2999, 'digital': False, 'category': 'Footwear', 'stock': 55, 'description': 'Trendy sneakers for casual wear', 'image': 'Footwear (2).jpg'},
    
    # Accessories
    {'name': 'Sunglasses', 'price': 1299, 'digital': False, 'category': 'Accessories', 'stock': 70, 'description': 'UV protection sunglasses with stylish design', 'image': 'Accessories.jpg'},
    {'name': 'Travel Backpack', 'price': 1999, 'digital': False, 'category': 'Accessories', 'stock': 35, 'description': 'Durable backpack with multiple compartments', 'image': 'Accessories (2).jpg'},
    {'name': 'Leather Wallet', 'price': 899, 'digital': False, 'category': 'Accessories', 'stock': 90, 'description': 'Premium leather wallet with card slots', 'image': 'Accessories (3).jpg'},
    {'name': 'Wrist Watch', 'price': 2499, 'digital': False, 'category': 'Accessories', 'stock': 45, 'description': 'Elegant wrist watch for formal occasions', 'image': 'Accessories (4).jpg'},
    {'name': 'Belt', 'price': 599, 'digital': False, 'category': 'Accessories', 'stock': 100, 'description': 'Genuine leather belt with metal buckle', 'image': 'Accessories (5).jpg'},
    {'name': 'Cap', 'price': 399, 'digital': False, 'category': 'Accessories', 'stock': 120, 'description': 'Stylish cap for outdoor activities', 'image': 'Accessories (6).jpg'},
    {'name': 'Scarf', 'price': 699, 'digital': False, 'category': 'Accessories', 'stock': 60, 'description': 'Soft woolen scarf for winter', 'image': 'Accessories (7).jpg'},
    {'name': 'Hand Gloves', 'price': 499, 'digital': False, 'category': 'Accessories', 'stock': 80, 'description': 'Warm hand gloves for cold weather', 'image': 'Accessories (8).jpg'},
    {'name': 'Tie', 'price': 599, 'digital': False, 'category': 'Accessories', 'stock': 75, 'description': 'Formal tie for business attire', 'image': 'Accessories (9).jpg'},
    {'name': 'Handbag', 'price': 2999, 'digital': False, 'category': 'Accessories', 'stock': 40, 'description': 'Designer handbag with spacious interior', 'image': 'Accessories (10).jpg'},
    {'name': 'Laptop Bag', 'price': 1499, 'digital': False, 'category': 'Accessories', 'stock': 50, 'description': 'Protective laptop bag with padding', 'image': 'Accessories (11).jpg'},
    {'name': 'Phone Case', 'price': 299, 'digital': False, 'category': 'Accessories', 'stock': 150, 'description': 'Durable phone case with shock protection', 'image': 'Accessories (12).jpg'},
    {'name': 'Earrings', 'price': 799, 'digital': False, 'category': 'Accessories', 'stock': 85, 'description': 'Elegant earrings for special occasions', 'image': 'Accessories (13).jpg'},
    {'name': 'Bracelet', 'price': 1299, 'digital': False, 'category': 'Accessories', 'stock': 65, 'description': 'Stylish bracelet with modern design', 'image': 'Accessories (14).jpg'},
    {'name': 'Necklace', 'price': 1999, 'digital': False, 'category': 'Accessories', 'stock': 55, 'description': 'Beautiful necklace for elegant look', 'image': 'Accessories (15).jpg'},
    {'name': 'Ring', 'price': 2499, 'digital': False, 'category': 'Accessories', 'stock': 70, 'description': 'Premium ring with gemstone', 'image': 'Accessories (16).jpg'},
    
    # Home & Kitchen
    {'name': 'Coffee Maker', 'price': 2999, 'digital': False, 'category': 'Home & Kitchen', 'stock': 35, 'description': 'Automatic coffee maker with timer', 'image': 'Home & Kitchen.jpg'},
    {'name': 'Blender', 'price': 1999, 'digital': False, 'category': 'Home & Kitchen', 'stock': 45, 'description': 'Powerful blender for smoothies and shakes', 'image': 'Home & Kitchen (2).jpg'},
    {'name': 'Cookware Set', 'price': 3499, 'digital': False, 'category': 'Home & Kitchen', 'stock': 30, 'description': 'Non-stick cookware set with lids', 'image': 'Home & Kitchen (3).jpg'},
    {'name': 'Dinner Set', 'price': 2499, 'digital': False, 'category': 'Home & Kitchen', 'stock': 40, 'description': 'Elegant dinner set for 6 people', 'image': 'Home & Kitchen (4).jpg'},
    
    # Furniture
    {'name': 'Gaming Chair', 'price': 12999, 'digital': False, 'category': 'Furniture', 'stock': 20, 'description': 'Ergonomic gaming chair with lumbar support', 'image': 'Furniture.jpg'},
    
    # Beauty
    {'name': 'Face Cream', 'price': 899, 'digital': False, 'category': 'Beauty', 'stock': 100, 'description': 'Moisturizing face cream for all skin types', 'image': 'Beauty.jpg'},
    {'name': 'Lipstick', 'price': 499, 'digital': False, 'category': 'Beauty', 'stock': 120, 'description': 'Long-lasting lipstick with vibrant colors', 'image': 'Beauty (2).jpg'},
    {'name': 'Perfume', 'price': 1999, 'digital': False, 'category': 'Beauty', 'stock': 60, 'description': 'Premium perfume with lasting fragrance', 'image': 'Beauty (3).jpg'},
    {'name': 'Hair Dryer', 'price': 1499, 'digital': False, 'category': 'Beauty', 'stock': 45, 'description': 'Professional hair dryer with multiple settings', 'image': 'Beauty (4).jpg'},
    {'name': 'Makeup Kit', 'price': 2499, 'digital': False, 'category': 'Beauty', 'stock': 50, 'description': 'Complete makeup kit with brushes', 'image': 'Beauty (5).jpg'},
    
    # Health
    {'name': 'Yoga Mat', 'price': 799, 'digital': False, 'category': 'Health', 'stock': 70, 'description': 'Non-slip yoga mat for exercise', 'image': 'Health.jpg'},
    {'name': 'Dumbbells Set', 'price': 1999, 'digital': False, 'category': 'Health', 'stock': 40, 'description': 'Adjustable dumbbells for home workout', 'image': 'Health (2).jpg'},
    
    # Books & Digital
    {'name': 'Programming Guide', 'price': 499, 'digital': True, 'category': 'Books', 'stock': 999, 'description': 'Complete guide to modern programming', 'image': 'Books.jpg'},
    {'name': 'Source Code Package', 'price': 1999, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'Premium source code templates and projects', 'image': 'Digital.jpg'},
    {'name': 'Web Design Course', 'price': 2999, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'Complete web design video course', 'image': 'Digital (2).jpg'},
]

Product.objects.all().delete()
print("Cleared existing products\n")

for data in PRODUCTS:
    product = Product.objects.create(**data)
    print(f"[+] {product.name} - Rs.{product.price} ({product.category})")

print(f"\n[SUCCESS] Total: {Product.objects.count()} products")
print(f"[INFO] Categories: {', '.join(Product.objects.values_list('category', flat=True).distinct())}")

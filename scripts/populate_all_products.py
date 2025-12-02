#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

PRODUCTS = [
    # Electronics
    {'name': 'Wireless Headphones', 'price': 2499, 'digital': False, 'category': 'Electronics', 'stock': 45, 'description': 'Premium wireless headphones with noise cancellation', 'image': 'images/headphone.jpg'},
    {'name': 'Smartwatch Pro', 'price': 3999, 'digital': False, 'category': 'Electronics', 'stock': 30, 'description': 'Fitness tracking smartwatch with heart rate monitor', 'image': 'images/Watch-1.jpg'},
    {'name': 'Classic Watch', 'price': 4999, 'digital': False, 'category': 'Electronics', 'stock': 25, 'description': 'Elegant analog watch for professionals', 'image': 'images/watch.jpg'},
    {'name': 'Bluetooth Speaker', 'price': 1899, 'digital': False, 'category': 'Electronics', 'stock': 50, 'description': 'Portable wireless speaker with rich bass', 'image': 'images/bluetooth_speaker.jpg'},
    {'name': 'Gaming Laptop', 'price': 54999, 'digital': False, 'category': 'Electronics', 'stock': 15, 'description': 'High-performance laptop for work and gaming', 'image': 'images/laptop.jpg'},
    {'name': 'ThinkPad X1', 'price': 89999, 'digital': False, 'category': 'Electronics', 'stock': 10, 'description': 'Business laptop with premium build quality', 'image': 'images/thinkpadx1.jpeg'},
    {'name': 'Dell Laptop', 'price': 45999, 'digital': False, 'category': 'Electronics', 'stock': 20, 'description': 'Reliable laptop for everyday computing', 'image': 'images/dell-yNvVnPcurD8-unsplash.jpg'},
    {'name': 'Smartphone', 'price': 29999, 'digital': False, 'category': 'Electronics', 'stock': 25, 'description': 'Latest smartphone with advanced camera system', 'image': 'images/smartphone.jpg'},
    {'name': 'OnePlus Phone', 'price': 34999, 'digital': False, 'category': 'Electronics', 'stock': 18, 'description': 'Fast charging flagship smartphone', 'image': 'images/phone-1.jpg'},
    {'name': 'Galaxy S24 Ultra', 'price': 124999, 'digital': False, 'category': 'Electronics', 'stock': 12, 'description': 'Premium flagship with S Pen', 'image': 'images/THUMB_Galaxy-S24ultra-MAThumb-1440x960.jpg'},
    {'name': 'Wireless Mouse', 'price': 799, 'digital': False, 'category': 'Electronics', 'stock': 60, 'description': 'Ergonomic wireless mouse with precision tracking', 'image': 'images/wireless_mouse.jpg'},
    {'name': 'Fitness Tracker', 'price': 2499, 'digital': False, 'category': 'Electronics', 'stock': 40, 'description': 'Smart fitness band with activity tracking', 'image': 'images/fitness_tracker.jpg'},
    
    # Clothing & Fashion
    {'name': 'Cotton T-Shirt', 'price': 599, 'digital': False, 'category': 'Clothing', 'stock': 100, 'description': 'Comfortable cotton t-shirt for everyday wear', 'image': 'images/tshirt.jpg'},
    {'name': 'Denim Jeans', 'price': 1499, 'digital': False, 'category': 'Clothing', 'stock': 75, 'description': 'Classic fit denim jeans with premium fabric', 'image': 'images/jeans.jpg'},
    {'name': 'Winter Hoodie', 'price': 1899, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Warm and cozy hoodie for winter', 'image': 'images/hoodie.jpg'},
    {'name': 'Premium Hoodie', 'price': 2499, 'digital': False, 'category': 'Clothing', 'stock': 40, 'description': 'Premium quality hoodie with soft fabric', 'image': 'images/hoddie-1.jpg'},
    {'name': 'Designer Dress', 'price': 3499, 'digital': False, 'category': 'Clothing', 'stock': 30, 'description': 'Elegant dress for special occasions', 'image': 'images/ashley-piszek-fL-tFsPhbco-unsplash.jpg'},
    {'name': 'Casual Shirt', 'price': 899, 'digital': False, 'category': 'Clothing', 'stock': 60, 'description': 'Comfortable casual shirt for daily wear', 'image': 'images/auguras-pipiras-O43D6CYzxqM-unsplash.jpg'},
    {'name': 'Summer Dress', 'price': 2999, 'digital': False, 'category': 'Clothing', 'stock': 35, 'description': 'Light and breezy summer dress', 'image': 'images/bosh-ar-1sSfrozgiFk-unsplash.jpg'},
    {'name': 'Formal Blazer', 'price': 4999, 'digital': False, 'category': 'Clothing', 'stock': 25, 'description': 'Professional blazer for office wear', 'image': 'images/bruno-yamazaky-x65f5vaY73I-unsplash.jpg'},
    {'name': 'Leather Jacket', 'price': 5999, 'digital': False, 'category': 'Clothing', 'stock': 20, 'description': 'Stylish leather jacket for bikers', 'image': 'images/cemrecan-yurtman-JVUqiEc2Svc-unsplash.jpg'},
    {'name': 'Polo T-Shirt', 'price': 799, 'digital': False, 'category': 'Clothing', 'stock': 70, 'description': 'Classic polo shirt for casual look', 'image': 'images/chris-lynch-SXpun7pdECU-unsplash.jpg'},
    {'name': 'Sports Jersey', 'price': 1299, 'digital': False, 'category': 'Clothing', 'stock': 45, 'description': 'Breathable sports jersey for athletes', 'image': 'images/chris-panas-UeITqYE-Xxw-unsplash.jpg'},
    {'name': 'Vintage Jacket', 'price': 3999, 'digital': False, 'category': 'Clothing', 'stock': 15, 'description': 'Retro style vintage jacket', 'image': 'images/claudio-schwarz-D3n859qG03U-unsplash.jpg'},
    {'name': 'Floral Dress', 'price': 2499, 'digital': False, 'category': 'Clothing', 'stock': 30, 'description': 'Beautiful floral print dress', 'image': 'images/emiliano-cicero-OKZqs-Vseko-unsplash.jpg'},
    {'name': 'Denim Jacket', 'price': 2999, 'digital': False, 'category': 'Clothing', 'stock': 35, 'description': 'Classic denim jacket for all seasons', 'image': 'images/habib-dadkhah-MivM1hirbUI-unsplash.jpg'},
    {'name': 'Striped Shirt', 'price': 1099, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Trendy striped casual shirt', 'image': 'images/hamed-darzi-Psz62UPYx1E-unsplash.jpg'},
    {'name': 'White Sneakers Outfit', 'price': 1799, 'digital': False, 'category': 'Clothing', 'stock': 40, 'description': 'Complete casual outfit with sneakers', 'image': 'images/insung-yoon-mru38VH7tII-unsplash.jpg'},
    {'name': 'Formal Suit', 'price': 8999, 'digital': False, 'category': 'Clothing', 'stock': 15, 'description': 'Premium formal suit for business', 'image': 'images/john-torcasio-TJrkkhdB39E-unsplash.jpg'},
    {'name': 'Casual Pants', 'price': 1499, 'digital': False, 'category': 'Clothing', 'stock': 55, 'description': 'Comfortable casual pants', 'image': 'images/jonathan-borba-af7c0GwLsGU-unsplash.jpg'},
    {'name': 'Street Style Hoodie', 'price': 2199, 'digital': False, 'category': 'Clothing', 'stock': 45, 'description': 'Urban street style hoodie', 'image': 'images/kadarius-seegars-FqVLT-Bs1jI-unsplash.jpg'},
    {'name': 'Bomber Jacket', 'price': 3499, 'digital': False, 'category': 'Clothing', 'stock': 25, 'description': 'Trendy bomber jacket', 'image': 'images/kadarius-seegars-RrL19hOvmgU-unsplash.jpg'},
    {'name': 'Checkered Shirt', 'price': 999, 'digital': False, 'category': 'Clothing', 'stock': 60, 'description': 'Classic checkered pattern shirt', 'image': 'images/karlis-reimanis-g1nmcKUtGQU-unsplash.jpg'},
    {'name': 'Beige Coat', 'price': 4499, 'digital': False, 'category': 'Clothing', 'stock': 20, 'description': 'Elegant beige winter coat', 'image': 'images/laura-chouette-NoqrVeKJCwE-unsplash.jpg'},
    {'name': 'Graphic Tee', 'price': 699, 'digital': False, 'category': 'Clothing', 'stock': 80, 'description': 'Cool graphic print t-shirt', 'image': 'images/luke-peterson-lUMj2Zv5HUE-unsplash.jpg'},
    {'name': 'Knit Sweater', 'price': 1999, 'digital': False, 'category': 'Clothing', 'stock': 40, 'description': 'Cozy knit sweater for cold days', 'image': 'images/mathilde-langevin-p3O5f4u95Lo-unsplash.jpg'},
    {'name': 'Puffer Jacket', 'price': 3999, 'digital': False, 'category': 'Clothing', 'stock': 30, 'description': 'Warm puffer jacket for winter', 'image': 'images/matthew-sleeper-Spdu7YT1O00-unsplash.jpg'},
    {'name': 'Trench Coat', 'price': 5499, 'digital': False, 'category': 'Clothing', 'stock': 18, 'description': 'Classic trench coat', 'image': 'images/maude-frederique-lavoie-EDSTj4kCUcw-unsplash.jpg'},
    {'name': 'Denim Shorts', 'price': 899, 'digital': False, 'category': 'Clothing', 'stock': 65, 'description': 'Comfortable denim shorts', 'image': 'images/nejc-soklic-g5Y5kjOwGwQ-unsplash.jpg'},
    {'name': 'Plaid Shirt', 'price': 1199, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Casual plaid pattern shirt', 'image': 'images/onur-binay-ZRAZhDk5zaE-unsplash.jpg'},
    {'name': 'Cargo Pants', 'price': 1799, 'digital': False, 'category': 'Clothing', 'stock': 45, 'description': 'Utility cargo pants with pockets', 'image': 'images/pavel-avakumov-D4p-eJcnNpQ-unsplash.jpg'},
    {'name': 'Linen Shirt', 'price': 1299, 'digital': False, 'category': 'Clothing', 'stock': 40, 'description': 'Breathable linen shirt for summer', 'image': 'images/richu-raphael-D7q4tPmOuCQ-unsplash.jpg'},
    {'name': 'Oversized Hoodie', 'price': 1899, 'digital': False, 'category': 'Clothing', 'stock': 50, 'description': 'Trendy oversized hoodie', 'image': 'images/robert-torres-XGs789r4lGg-unsplash.jpg'},
    {'name': 'Ethnic Wear', 'price': 2999, 'digital': False, 'category': 'Clothing', 'stock': 25, 'description': 'Traditional ethnic clothing', 'image': 'images/rubaitul-azad-ZIPFteu-R8k-unsplash.jpg'},
    {'name': 'Casual Blazer', 'price': 3499, 'digital': False, 'category': 'Clothing', 'stock': 30, 'description': 'Smart casual blazer', 'image': 'images/sanju-pandita-Sg0szdvF8-Q-unsplash.jpg'},
    {'name': 'Printed Shirt', 'price': 999, 'digital': False, 'category': 'Clothing', 'stock': 55, 'description': 'Colorful printed casual shirt', 'image': 'images/sayan-majhi-vOeF4zZS8rE-unsplash.jpg'},
    {'name': 'Formal Pants', 'price': 1699, 'digital': False, 'category': 'Clothing', 'stock': 45, 'description': 'Professional formal pants', 'image': 'images/steven-erixon-v_mf1iidtnk-unsplash.jpg'},
    {'name': 'Sweatshirt', 'price': 1499, 'digital': False, 'category': 'Clothing', 'stock': 60, 'description': 'Comfortable sweatshirt', 'image': 'images/triyansh-gill-VAfKv0MPzjg-unsplash.jpg'},
    {'name': 'Cardigan', 'price': 1799, 'digital': False, 'category': 'Clothing', 'stock': 35, 'description': 'Cozy cardigan sweater', 'image': 'images/valeriia-miller-_42NKYROG7g-unsplash.jpg'},
    {'name': 'Track Pants', 'price': 1299, 'digital': False, 'category': 'Clothing', 'stock': 70, 'description': 'Athletic track pants', 'image': 'images/yash-parashar-LWPPpkn6NEQ-unsplash.jpg'},
    
    # Footwear
    {'name': 'Running Shoes', 'price': 3499, 'digital': False, 'category': 'Footwear', 'stock': 40, 'description': 'Lightweight running shoes with cushioned sole', 'image': 'images/shoe.jpg'},
    {'name': 'White Sneakers', 'price': 2999, 'digital': False, 'category': 'Footwear', 'stock': 55, 'description': 'Trendy white sneakers for casual wear', 'image': 'images/sneakers.jpg'},
    {'name': 'Sports Shoes', 'price': 3999, 'digital': False, 'category': 'Footwear', 'stock': 35, 'description': 'Professional sports shoes', 'image': 'images/pexels-godisable-jacob-226636-934673.jpg'},
    
    # Accessories
    {'name': 'Sunglasses', 'price': 1299, 'digital': False, 'category': 'Accessories', 'stock': 70, 'description': 'UV protection sunglasses with stylish design', 'image': 'images/sunglasses.jpg'},
    {'name': 'Travel Backpack', 'price': 1999, 'digital': False, 'category': 'Accessories', 'stock': 35, 'description': 'Durable backpack with multiple compartments', 'image': 'images/backpack.jpg'},
    {'name': 'Camera Bag', 'price': 2499, 'digital': False, 'category': 'Accessories', 'stock': 25, 'description': 'Professional camera bag', 'image': 'images/ben-iwara-0i6igxIF2g8-unsplash.jpg'},
    {'name': 'Leather Wallet', 'price': 899, 'digital': False, 'category': 'Accessories', 'stock': 80, 'description': 'Premium leather wallet', 'image': 'images/gab-mWSXyWe2H9Q-unsplash.jpg'},
    {'name': 'Designer Handbag', 'price': 4999, 'digital': False, 'category': 'Accessories', 'stock': 20, 'description': 'Luxury designer handbag', 'image': 'images/grant-ritchie-n_wXNttWVGs-unsplash.jpg'},
    {'name': 'Laptop Bag', 'price': 1499, 'digital': False, 'category': 'Accessories', 'stock': 45, 'description': 'Protective laptop carrying bag', 'image': 'images/hannes-kottner-Wxc0hAt0nQI-unsplash.jpg'},
    {'name': 'Tote Bag', 'price': 799, 'digital': False, 'category': 'Accessories', 'stock': 60, 'description': 'Stylish tote bag for shopping', 'image': 'images/john-m-smit-Mc5EwlPC3zA-unsplash.jpg'},
    {'name': 'Crossbody Bag', 'price': 1299, 'digital': False, 'category': 'Accessories', 'stock': 50, 'description': 'Compact crossbody bag', 'image': 'images/kelly-sikkema-IZOAOjvwhaM-unsplash.jpg'},
    {'name': 'Clutch Purse', 'price': 999, 'digital': False, 'category': 'Accessories', 'stock': 40, 'description': 'Elegant clutch for parties', 'image': 'images/klaudia-piaskowska-Zy6oNZRdcjc-unsplash.jpg'},
    {'name': 'Shoulder Bag', 'price': 1799, 'digital': False, 'category': 'Accessories', 'stock': 35, 'description': 'Comfortable shoulder bag', 'image': 'images/lazar-gugleta-Ub4CggGYf2o-unsplash.jpg'},
    {'name': 'Mini Backpack', 'price': 1199, 'digital': False, 'category': 'Accessories', 'stock': 45, 'description': 'Cute mini backpack', 'image': 'images/olga-kovalski-p2JOmn_V3YU-unsplash.jpg'},
    {'name': 'Belt', 'price': 599, 'digital': False, 'category': 'Accessories', 'stock': 90, 'description': 'Leather belt for formal wear', 'image': 'images/pat-taylor-12V36G17IbQ-unsplash.jpg'},
    {'name': 'Scarf', 'price': 699, 'digital': False, 'category': 'Accessories', 'stock': 70, 'description': 'Warm winter scarf', 'image': 'images/thai-nguyen-UrIe7dzoVcU-unsplash.jpg'},
    
    # Beauty & Personal Care
    {'name': 'Skincare Set', 'price': 1999, 'digital': False, 'category': 'Beauty', 'stock': 40, 'description': 'Complete skincare routine set', 'image': 'images/curology-SjqgfcH207A-unsplash.jpg'},
    {'name': 'Perfume', 'price': 2499, 'digital': False, 'category': 'Beauty', 'stock': 50, 'description': 'Premium fragrance perfume', 'image': 'images/onne-beauty-6cGnT43v7PE-unsplash.jpg'},
    {'name': 'Makeup Kit', 'price': 3499, 'digital': False, 'category': 'Beauty', 'stock': 30, 'description': 'Professional makeup kit', 'image': 'images/pexels-ekrulila-2452345.jpg'},
    
    # Health & Nutrition
    {'name': 'Protein Shake', 'price': 1499, 'digital': False, 'category': 'Health', 'stock': 60, 'description': 'Nutritious protein shake mix', 'image': 'images/ctrl-a-meal-replacement-a_Q3fPs3qLs-unsplash.jpg'},
    {'name': 'Vitamin Supplements', 'price': 999, 'digital': False, 'category': 'Health', 'stock': 80, 'description': 'Daily vitamin supplements', 'image': 'images/gold-touch-nutrition-UTrei2MZkss-unsplash.jpg'},
    
    # Home & Kitchen
    {'name': 'Coffee Mug', 'price': 299, 'digital': False, 'category': 'Home & Kitchen', 'stock': 100, 'description': 'Ceramic coffee mug with elegant design', 'image': 'images/coffee_mug.jpg'},
    {'name': 'Plant Pot', 'price': 399, 'digital': False, 'category': 'Home & Kitchen', 'stock': 80, 'description': 'Modern ceramic pot for indoor plants', 'image': 'images/plant_pot.jpg'},
    {'name': 'Decorative Vase', 'price': 799, 'digital': False, 'category': 'Home & Kitchen', 'stock': 50, 'description': 'Elegant decorative vase', 'image': 'images/pexels-bertellifotografia-2905238.jpg'},
    {'name': 'Candle Set', 'price': 599, 'digital': False, 'category': 'Home & Kitchen', 'stock': 70, 'description': 'Aromatic candle set', 'image': 'images/pexels-bohlemedia-1102874.jpg'},
    
    # Furniture
    {'name': 'Gaming Chair', 'price': 12999, 'digital': False, 'category': 'Furniture', 'stock': 20, 'description': 'Ergonomic gaming chair with lumbar support', 'image': 'images/gaming_chair.jpg'},
    
    # Books & Digital
    {'name': 'Programming Guide', 'price': 499, 'digital': True, 'category': 'Books', 'stock': 999, 'description': 'Complete guide to modern programming', 'image': 'images/book.jpg'},
    {'name': 'Design Book', 'price': 599, 'digital': True, 'category': 'Books', 'stock': 999, 'description': 'Professional design principles book', 'image': 'images/Book-1.jpg'},
    {'name': 'Source Code Package', 'price': 1999, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'Premium source code templates and projects', 'image': 'images/source_code.jpg'},
    
    # Stationery & Office
    {'name': 'Notebook Set', 'price': 399, 'digital': False, 'category': 'Stationery', 'stock': 100, 'description': 'Premium quality notebooks', 'image': 'images/daniel-korpai-QhF3YGsDrYk-unsplash.jpg'},
    {'name': 'Desk Organizer', 'price': 699, 'digital': False, 'category': 'Stationery', 'stock': 60, 'description': 'Wooden desk organizer', 'image': 'images/daniel-maquiling-vfAQkN3WbwU-unsplash.jpg'},
    {'name': 'Pen Set', 'price': 499, 'digital': False, 'category': 'Stationery', 'stock': 80, 'description': 'Premium pen collection', 'image': 'images/daniel-schludi-7J-ro9TbEp0-unsplash.jpg'},
    
    # Pet Products
    {'name': 'Dog Toy', 'price': 299, 'digital': False, 'category': 'Pets', 'stock': 90, 'description': 'Durable dog chew toy', 'image': 'images/charlesdeluvio-1-nx1QR5dTE-unsplash.jpg'},
    
    # Art & Craft
    {'name': 'Art Supplies', 'price': 1499, 'digital': False, 'category': 'Art', 'stock': 40, 'description': 'Complete art supplies kit', 'image': 'images/shreesha-bhat-lz6z9GZu8hk-unsplash.jpg'},
    {'name': 'Craft Materials', 'price': 899, 'digital': False, 'category': 'Art', 'stock': 50, 'description': 'DIY craft materials set', 'image': 'images/sun-lingyan-_H0fjILH5Vw-unsplash.jpg'},
    
    # Mockups & Templates
    {'name': 'T-Shirt Mockup', 'price': 299, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'Professional t-shirt mockup template', 'image': 'images/mockup-free-opAeFlgyQqs-unsplash.jpg'},
    {'name': 'Poster Mockup', 'price': 399, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'High-quality poster mockup', 'image': 'images/mockup-free-pHEtQf8Q5nk-unsplash.jpg'},
    {'name': 'Brand Identity Kit', 'price': 1999, 'digital': True, 'category': 'Digital', 'stock': 999, 'description': 'Complete brand identity templates', 'image': 'images/project-290-PTorAkUcYHg-unsplash.jpg'},
    
    # Additional Products
    {'name': 'Wireless Earbuds', 'price': 1999, 'digital': False, 'category': 'Electronics', 'stock': 50, 'description': 'True wireless earbuds with charging case', 'image': 'images/download (2).jpeg'},
    {'name': 'Smart Speaker', 'price': 3499, 'digital': False, 'category': 'Electronics', 'stock': 35, 'description': 'Voice-controlled smart speaker', 'image': 'images/download (3).jpeg'},
    {'name': 'Premium Laptop', 'price': 79999, 'digital': False, 'category': 'Electronics', 'stock': 12, 'description': 'High-end laptop for professionals', 'image': 'images/istockphoto-1503144234-612x612.webp'},
    {'name': 'Modern Smartphone', 'price': 39999, 'digital': False, 'category': 'Electronics', 'stock': 22, 'description': 'Latest generation smartphone', 'image': 'images/photo-1677047642886-a20fa832456e.avif'},
    {'name': 'Minimalist Watch', 'price': 2999, 'digital': False, 'category': 'Accessories', 'stock': 40, 'description': 'Sleek minimalist wristwatch', 'image': 'images/wiser-by-the-mile-SwWCo1k92M4-unsplash.jpg'},
    {'name': 'Fashion Sunglasses', 'price': 1499, 'digital': False, 'category': 'Accessories', 'stock': 55, 'description': 'Trendy fashion sunglasses', 'image': 'images/zakkaria-ahmed-2oVsOVqTdu4-unsplash.jpg'},
]

def populate():
    Product.objects.all().delete()
    print("Cleared existing products\n")
    
    for data in PRODUCTS:
        product = Product.objects.create(**data)
        print(f"[+] {product.name} - Rs.{product.price}")
    
    print(f"\n[SUCCESS] Total: {Product.objects.count()} products")
    categories = Product.objects.values_list('category', flat=True).distinct()
    print(f"[INFO] Categories: {', '.join(categories)}")

if __name__ == '__main__':
    populate()

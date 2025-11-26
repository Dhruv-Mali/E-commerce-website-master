import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

# Clear existing products
Product.objects.all().delete()

products_data = [
    # Electronics - Smartphones
    {"name": "iPhone 15 Pro Max", "price": 134900, "category": "Electronics", "description": "Latest Apple flagship with A17 Pro chip, titanium design, and advanced camera system", "stock": 25, "digital": False, "image": "placeholder.jpg"},
    {"name": "Samsung Galaxy S24 Ultra", "price": 124999, "category": "Electronics", "description": "Premium Android phone with S Pen, 200MP camera, and AI features", "stock": 30, "digital": False, "image": "placeholder.jpg"},
    {"name": "Google Pixel 8 Pro", "price": 84999, "category": "Electronics", "description": "Google's flagship with advanced AI photography and pure Android experience", "stock": 20, "digital": False, "image": "placeholder.jpg"},
    {"name": "OnePlus 12", "price": 64999, "category": "Electronics", "description": "Flagship killer with Snapdragon 8 Gen 3 and 100W fast charging", "stock": 35, "digital": False, "image": "placeholder.jpg"},
    {"name": "Xiaomi 14 Pro", "price": 54999, "category": "Electronics", "description": "Premium phone with Leica cameras and stunning display", "stock": 40, "digital": False, "image": "placeholder.jpg"},
    
    # Electronics - Laptops
    {"name": "MacBook Pro 16 M3", "price": 249900, "category": "Electronics", "description": "Powerful laptop for professionals with M3 Max chip and stunning display", "stock": 15, "digital": False, "image": "placeholder.jpg"},
    {"name": "Dell XPS 15", "price": 159999, "category": "Electronics", "description": "Premium Windows laptop with 4K OLED display and Intel Core i9", "stock": 20, "digital": False, "image": "placeholder.jpg"},
    {"name": "HP Spectre x360", "price": 134999, "category": "Electronics", "description": "Convertible laptop with gem-cut design and long battery life", "stock": 18, "digital": False, "image": "placeholder.jpg"},
    {"name": "Lenovo ThinkPad X1", "price": 124999, "category": "Electronics", "description": "Business laptop with legendary keyboard and durability", "stock": 25, "digital": False, "image": "placeholder.jpg"},
    {"name": "ASUS ROG Zephyrus", "price": 179999, "category": "Electronics", "description": "Gaming laptop with RTX 4080 and 240Hz display", "stock": 12, "digital": False, "image": "placeholder.jpg"},
    
    # Electronics - Headphones
    {"name": "Sony WH-1000XM5", "price": 29990, "category": "Electronics", "description": "Industry-leading noise cancellation with premium sound quality", "stock": 50, "digital": False, "image": "headphone.jpg"},
    {"name": "AirPods Pro 2", "price": 24900, "category": "Electronics", "description": "Apple's premium earbuds with adaptive audio and USB-C", "stock": 60, "digital": False, "image": "placeholder.jpg"},
    {"name": "Bose QuietComfort Ultra", "price": 34990, "category": "Electronics", "description": "Premium headphones with spatial audio and all-day comfort", "stock": 35, "digital": False, "image": "placeholder.jpg"},
    {"name": "JBL Tune 770NC", "price": 7999, "category": "Electronics", "description": "Budget-friendly ANC headphones with great battery life", "stock": 80, "digital": False, "image": "placeholder.jpg"},
    
    # Electronics - Smartwatches
    {"name": "Apple Watch Series 9", "price": 41900, "category": "Electronics", "description": "Advanced health tracking with always-on display", "stock": 45, "digital": False, "image": "watch.jpg"},
    {"name": "Samsung Galaxy Watch 6", "price": 29999, "category": "Electronics", "description": "Comprehensive fitness tracking with Wear OS", "stock": 40, "digital": False, "image": "placeholder.jpg"},
    {"name": "Garmin Fenix 7", "price": 64999, "category": "Electronics", "description": "Premium multisport GPS watch for athletes", "stock": 20, "digital": False, "image": "placeholder.jpg"},
    {"name": "Fitbit Sense 2", "price": 19999, "category": "Electronics", "description": "Health-focused smartwatch with stress management", "stock": 55, "digital": False, "image": "placeholder.jpg"},
    
    # Fashion - Men's Clothing
    {"name": "Levi's 501 Original Jeans", "price": 3999, "category": "Fashion", "description": "Classic straight fit jeans in premium denim", "stock": 100, "digital": False, "image": "placeholder.jpg"},
    {"name": "Nike Dri-FIT T-Shirt", "price": 1499, "category": "Fashion", "description": "Moisture-wicking athletic tee for workouts", "stock": 150, "digital": False, "image": "tshirt.jpg"},
    {"name": "Adidas Originals Hoodie", "price": 4999, "category": "Fashion", "description": "Comfortable cotton hoodie with iconic trefoil logo", "stock": 80, "digital": False, "image": "placeholder.jpg"},
    {"name": "Tommy Hilfiger Polo", "price": 3499, "category": "Fashion", "description": "Classic polo shirt in premium cotton pique", "stock": 90, "digital": False, "image": "placeholder.jpg"},
    {"name": "Zara Slim Fit Blazer", "price": 7999, "category": "Fashion", "description": "Modern blazer for formal and casual occasions", "stock": 45, "digital": False, "image": "placeholder.jpg"},
    
    # Fashion - Women's Clothing
    {"name": "H&M Floral Dress", "price": 2999, "category": "Fashion", "description": "Elegant summer dress with floral print", "stock": 70, "digital": False, "image": "placeholder.jpg"},
    {"name": "Forever 21 Crop Top", "price": 999, "category": "Fashion", "description": "Trendy crop top in various colors", "stock": 120, "digital": False, "image": "placeholder.jpg"},
    {"name": "Mango Leather Jacket", "price": 12999, "category": "Fashion", "description": "Premium faux leather jacket with modern cut", "stock": 35, "digital": False, "image": "placeholder.jpg"},
    {"name": "Uniqlo Cashmere Sweater", "price": 5999, "category": "Fashion", "description": "Soft cashmere blend sweater for winter", "stock": 60, "digital": False, "image": "placeholder.jpg"},
    
    # Footwear
    {"name": "Nike Air Max 270", "price": 12995, "category": "Footwear", "description": "Iconic sneakers with visible Air cushioning", "stock": 75, "digital": False, "image": "shoe.jpg"},
    {"name": "Adidas Ultraboost 23", "price": 16999, "category": "Footwear", "description": "Premium running shoes with Boost technology", "stock": 60, "digital": False, "image": "placeholder.jpg"},
    {"name": "Puma RS-X", "price": 8999, "category": "Footwear", "description": "Retro-inspired chunky sneakers", "stock": 85, "digital": False, "image": "placeholder.jpg"},
    {"name": "Converse Chuck Taylor", "price": 4999, "category": "Footwear", "description": "Classic canvas sneakers in high-top style", "stock": 100, "digital": False, "image": "placeholder.jpg"},
    {"name": "Clarks Desert Boots", "price": 9999, "category": "Footwear", "description": "Timeless suede boots for casual wear", "stock": 50, "digital": False, "image": "placeholder.jpg"},
    
    # Books
    {"name": "Atomic Habits by James Clear", "price": 599, "category": "Books", "description": "Transform your life with tiny changes that deliver remarkable results", "stock": 200, "digital": False, "image": "book.jpg"},
    {"name": "The Psychology of Money", "price": 499, "category": "Books", "description": "Timeless lessons on wealth, greed, and happiness", "stock": 180, "digital": False, "image": "placeholder.jpg"},
    {"name": "Sapiens by Yuval Noah Harari", "price": 699, "category": "Books", "description": "A brief history of humankind", "stock": 150, "digital": False, "image": "placeholder.jpg"},
    {"name": "Think Like a Monk", "price": 549, "category": "Books", "description": "Train your mind for peace and purpose", "stock": 160, "digital": False, "image": "placeholder.jpg"},
    {"name": "Rich Dad Poor Dad", "price": 399, "category": "Books", "description": "What the rich teach their kids about money", "stock": 220, "digital": False, "image": "placeholder.jpg"},
    
    # Home & Kitchen
    {"name": "Philips Air Fryer", "price": 8999, "category": "Home & Kitchen", "description": "Healthy cooking with rapid air technology", "stock": 40, "digital": False, "image": "placeholder.jpg"},
    {"name": "Prestige Induction Cooktop", "price": 2999, "category": "Home & Kitchen", "description": "Energy-efficient cooking with touch controls", "stock": 55, "digital": False, "image": "placeholder.jpg"},
    {"name": "Borosil Glass Dinner Set", "price": 1999, "category": "Home & Kitchen", "description": "Microwave-safe glass dinnerware set of 12", "stock": 70, "digital": False, "image": "placeholder.jpg"},
    {"name": "Amazon Echo Dot 5", "price": 4499, "category": "Home & Kitchen", "description": "Smart speaker with Alexa voice control", "stock": 90, "digital": False, "image": "placeholder.jpg"},
    {"name": "Dyson V12 Vacuum", "price": 44999, "category": "Home & Kitchen", "description": "Cordless vacuum with laser detection", "stock": 25, "digital": False, "image": "placeholder.jpg"},
    
    # Sports & Fitness
    {"name": "Yoga Mat Premium", "price": 1299, "category": "Sports & Fitness", "description": "Non-slip exercise mat with carrying strap", "stock": 100, "digital": False, "image": "placeholder.jpg"},
    {"name": "Dumbbells Set 20kg", "price": 3999, "category": "Sports & Fitness", "description": "Adjustable dumbbells for home workouts", "stock": 45, "digital": False, "image": "placeholder.jpg"},
    {"name": "Resistance Bands Set", "price": 799, "category": "Sports & Fitness", "description": "5-piece resistance band set for strength training", "stock": 120, "digital": False, "image": "placeholder.jpg"},
    {"name": "Protein Shaker Bottle", "price": 299, "category": "Sports & Fitness", "description": "Leak-proof shaker with mixing ball", "stock": 200, "digital": False, "image": "placeholder.jpg"},
    
    # Beauty & Personal Care
    {"name": "Lakme Eyeconic Kajal", "price": 225, "category": "Beauty", "description": "Smudge-proof kajal with intense black color", "stock": 300, "digital": False, "image": "placeholder.jpg"},
    {"name": "Mamaearth Face Wash", "price": 349, "category": "Beauty", "description": "Natural face wash with vitamin C", "stock": 250, "digital": False, "image": "placeholder.jpg"},
    {"name": "Gillette Fusion Razor", "price": 599, "category": "Beauty", "description": "5-blade razor for smooth shave", "stock": 180, "digital": False, "image": "placeholder.jpg"},
    {"name": "Nivea Body Lotion", "price": 299, "category": "Beauty", "description": "Moisturizing lotion for soft skin", "stock": 220, "digital": False, "image": "placeholder.jpg"},
    
    # Digital Products
    {"name": "Python Programming Course", "price": 1999, "category": "Digital", "description": "Complete Python course from beginner to advanced", "stock": 999, "digital": True, "image": "source_code.jpg"},
    {"name": "Web Development Bootcamp", "price": 2999, "category": "Digital", "description": "Full-stack web development course with projects", "stock": 999, "digital": True, "image": "placeholder.jpg"},
    {"name": "Photoshop Masterclass", "price": 1499, "category": "Digital", "description": "Professional photo editing course", "stock": 999, "digital": True, "image": "placeholder.jpg"},
    {"name": "Digital Marketing Guide", "price": 999, "category": "Digital", "description": "Complete guide to social media and SEO", "stock": 999, "digital": True, "image": "placeholder.jpg"},
]

print("Creating products...")
for product_data in products_data:
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults=product_data
    )
    if created:
        print(f"[+] Created: {product.name}")
    else:
        print(f"[-] Exists: {product.name}")

print(f"\n[SUCCESS] Total products in database: {Product.objects.count()}")
print(f"[INFO] Categories: {', '.join(Product.objects.values_list('category', flat=True).distinct())}")

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

products_data = [
    {"name": "Premium Leather Wallet", "price": 1299, "category": "Accessories", "image": "images/alex-lvrs-2zDw14yCYqk-unsplash.jpg", "stock": 50},
    {"name": "Designer Handbag", "price": 3499, "category": "Fashion", "image": "images/alexander-andrews-anUOLC3zMD4-unsplash.jpg", "stock": 30},
    {"name": "Luxury Watch", "price": 8999, "category": "Accessories", "image": "images/ali-saadat-ikLELWYbyxk-unsplash.jpg", "stock": 20},
    {"name": "Casual Sneakers", "price": 2499, "category": "Footwear", "image": "images/anh-nhat-PdALQmfEqvE-unsplash.jpg", "stock": 60},
    {"name": "Sports Shoes", "price": 3299, "category": "Footwear", "image": "images/anomaly-WWesmHEgXDs-unsplash.jpg", "stock": 45},
    {"name": "Vintage Camera", "price": 12999, "category": "Electronics", "image": "images/ashley-piszek-fL-tFsPhbco-unsplash.jpg", "stock": 15},
    {"name": "Professional Headphones", "price": 4599, "category": "Electronics", "image": "images/auguras-pipiras-O43D6CYzxqM-unsplash.jpg", "stock": 35},
    {"name": "Gaming Keyboard", "price": 3799, "category": "Electronics", "image": "images/ben-iwara-0i6igxIF2g8-unsplash.jpg", "stock": 40},
    {"name": "Skincare Set", "price": 1899, "category": "Beauty", "image": "images/curology-SjqgfcH3207A-unsplash.jpg", "stock": 55},
    {"name": "Protein Powder", "price": 2299, "category": "Health", "image": "images/ctrl-a-meal-replacement-a_Q3fPs3qLs-unsplash.jpg", "stock": 70},
    {"name": "Mechanical Keyboard", "price": 5499, "category": "Electronics", "image": "images/daniel-korpai-QhF3YGsDrYk-unsplash.jpg", "stock": 25},
    {"name": "Wireless Earbuds", "price": 2999, "category": "Electronics", "image": "images/daniel-maquiling-vfAQkN3WbwU-unsplash.jpg", "stock": 80},
    {"name": "Smart Speaker", "price": 3499, "category": "Electronics", "image": "images/daniel-schludi-7J-ro9TbEp0-unsplash.jpg", "stock": 50},
    {"name": "Dell Laptop", "price": 54999, "category": "Electronics", "image": "images/dell-yNvVnPcurD8-unsplash.jpg", "stock": 12},
    {"name": "Fitness Supplement", "price": 1599, "category": "Health", "image": "images/gold-touch-nutrition-UTrei2MZkss-unsplash.jpg", "stock": 90},
    {"name": "Designer Perfume", "price": 4299, "category": "Beauty", "image": "images/laura-chouette-NoqrVeKJCwE-unsplash.jpg", "stock": 40},
    {"name": "Luxury Perfume", "price": 5999, "category": "Beauty", "image": "images/onne-beauty-6cGnT43v7PE-unsplash.jpg", "stock": 30},
    {"name": "Makeup Kit", "price": 2799, "category": "Beauty", "image": "images/onur-binay-ZRAZhDk5zaE-unsplash.jpg", "stock": 45},
    {"name": "Yoga Mat", "price": 899, "category": "Fitness", "image": "images/klaudia-piaskowska-Zy6oNZRdcjc-unsplash.jpg", "stock": 65},
    {"name": "Running Shoes Pro", "price": 4299, "category": "Footwear", "image": "images/kadarius-seegars-FqVLT-Bs1jI-unsplash.jpg", "stock": 35},
    {"name": "Athletic Shoes", "price": 3899, "category": "Footwear", "image": "images/kadarius-seegars-RrL19hOvmgU-unsplash.jpg", "stock": 40},
    {"name": "Stylish Sunglasses", "price": 1499, "category": "Accessories", "image": "images/karlis-reimanis-g1nmcKUtGQU-unsplash.jpg", "stock": 55},
    {"name": "Notebook Set", "price": 599, "category": "Stationery", "image": "images/kelly-sikkema-IZOAOjvwhaM-unsplash.jpg", "stock": 100},
    {"name": "Desk Organizer", "price": 799, "category": "Home", "image": "images/mockup-free-opAeFlgyQqs-unsplash.jpg", "stock": 70},
    {"name": "Wall Clock", "price": 1299, "category": "Home", "image": "images/mockup-free-pHEtQf8Q5nk-unsplash.jpg", "stock": 45},
    {"name": "Ceramic Vase", "price": 1899, "category": "Home", "image": "images/olga-kovalski-p2JOmn_V3YU-unsplash.jpg", "stock": 30},
    {"name": "Decorative Candles", "price": 699, "category": "Home", "image": "images/pat-taylor-12V36G17IbQ-unsplash.jpg", "stock": 85},
    {"name": "Wireless Charger", "price": 1499, "category": "Electronics", "image": "images/pavel-avakumov-D4p-eJcnNpQ-unsplash.jpg", "stock": 60},
    {"name": "Camera Lens", "price": 18999, "category": "Electronics", "image": "images/pexels-bertellifotografia-2905238.jpg", "stock": 10},
    {"name": "DSLR Camera", "price": 45999, "category": "Electronics", "image": "images/pexels-bohlemedia-1102874.jpg", "stock": 8},
    {"name": "Camera Accessories", "price": 2499, "category": "Electronics", "image": "images/pexels-ekrulila-2452345.jpg", "stock": 35},
    {"name": "Fashion Sneakers", "price": 2899, "category": "Footwear", "image": "images/pexels-godisable-jacob-226636-934673.jpg", "stock": 50},
    {"name": "Minimalist Watch", "price": 6499, "category": "Accessories", "image": "images/project-290-PTorAkUcYHg-unsplash.jpg", "stock": 25},
    {"name": "Smart Band", "price": 2199, "category": "Electronics", "image": "images/richu-raphael-D7q4tPmOuCQ-unsplash.jpg", "stock": 55},
    {"name": "Portable Speaker", "price": 2799, "category": "Electronics", "image": "images/robert-torres-XGs789r4lGg-unsplash.jpg", "stock": 45},
    {"name": "Premium Headset", "price": 5299, "category": "Electronics", "image": "images/rubaitul-azad-ZIPFteu-R8k-unsplash.jpg", "stock": 30},
    {"name": "Facial Cream", "price": 1299, "category": "Beauty", "image": "images/sanju-pandita-Sg0szdvF8-Q-unsplash.jpg", "stock": 60},
    {"name": "Beauty Serum", "price": 1799, "category": "Beauty", "image": "images/sayan-majhi-vOeF4zZS8rE-unsplash.jpg", "stock": 50},
    {"name": "Luxury Shoes", "price": 7999, "category": "Footwear", "image": "images/shreesha-bhat-lz6z9GZu8hk-unsplash.jpg", "stock": 20},
    {"name": "Gaming Mouse", "price": 2499, "category": "Electronics", "image": "images/steven-erixon-v_mf1iidtnk-unsplash.jpg", "stock": 55},
    {"name": "Desk Lamp Pro", "price": 1899, "category": "Home", "image": "images/sun-lingyan-_H0fjILH5Vw-unsplash.jpg", "stock": 40},
    {"name": "USB Hub", "price": 899, "category": "Electronics", "image": "images/thai-nguyen-UrIe7dzoVcU-unsplash.jpg", "stock": 75},
    {"name": "ThinkPad X1", "price": 89999, "category": "Electronics", "image": "images/thinkpadx1.jpeg", "stock": 5},
    {"name": "Galaxy S24 Ultra", "price": 124999, "category": "Electronics", "image": "images/THUMB_Galaxy-S24ultra-MAThumb-1440x960.jpg", "stock": 10},
    {"name": "Designer Bag", "price": 4999, "category": "Fashion", "image": "images/triyansh-gill-VAfKv0MPzjg-unsplash.jpg", "stock": 25},
    {"name": "Cosmetic Set", "price": 3299, "category": "Beauty", "image": "images/valeriia-miller-_42NKYROG7g-unsplash.jpg", "stock": 35},
    {"name": "Protein Shake", "price": 1899, "category": "Health", "image": "images/wiser-by-the-mile-SwWCo1k92M4-unsplash.jpg", "stock": 80},
    {"name": "Fitness Band", "price": 1599, "category": "Electronics", "image": "images/yash-parashar-LWPPpkn6NEQ-unsplash.jpg", "stock": 60},
    {"name": "Smart Home Device", "price": 3999, "category": "Electronics", "image": "images/zakkaria-ahmed-2oVsOVqTdu4-unsplash.jpg", "stock": 30},
]

print("Adding products to database...")
added = 0
for data in products_data:
    if not Product.objects.filter(name=data['name']).exists():
        Product.objects.create(
            name=data['name'],
            price=data['price'],
            category=data['category'],
            image=data['image'],
            stock=data['stock'],
            description=f"High quality {data['name']} available now. Limited stock!",
            digital=False
        )
        added += 1
        print(f"[+] Added: {data['name']}")
    else:
        print(f"[-] Skipped: {data['name']} (already exists)")

print(f"\n[SUCCESS] Added {added} new products!")
print(f"Total products in database: {Product.objects.count()}")

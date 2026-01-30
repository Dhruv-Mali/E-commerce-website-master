# Database Verification Commands
# Run: python manage.py shell < db_check_commands.py

from django.db import connection
from apps.store.models import *
from apps.store.models_extended import *

print("\n" + "="*60)
print("DATABASE VERIFICATION")
print("="*60)

# 1. Connection Test
print("\n1. DATABASE CONNECTION:")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        print(f"   MySQL Version: {cursor.fetchone()[0]}")
        cursor.execute("SELECT DATABASE()")
        print(f"   Database: {cursor.fetchone()[0]}")
        cursor.execute("SHOW TABLES")
        print(f"   Tables: {len(cursor.fetchall())}")
    print("   Status: CONNECTED")
except Exception as e:
    print(f"   ERROR: {e}")

# 2. Table Counts
print("\n2. TABLE RECORD COUNTS:")
tables = {
    'Products': Product.objects.count(),
    'Customers': Customer.objects.count(),
    'Orders': Order.objects.count(),
    'Order Items': OrderItem.objects.count(),
    'Reviews': ProductReview.objects.count(),
    'Wishlist': Wishlist.objects.count(),
    'Coupons': Coupon.objects.count(),
    'Newsletter': Newsletter.objects.count(),
    'Recently Viewed': RecentlyViewed.objects.count(),
}
for name, count in tables.items():
    print(f"   {name:20}: {count} records")

# 3. Sample Data
print("\n3. SAMPLE DATA:")
if Product.objects.exists():
    p = Product.objects.first()
    print(f"   Product: {p.name} - Rs.{p.price}")
    print(f"   Stock: {p.stock}, Digital: {p.digital}")

if ProductReview.objects.exists():
    r = ProductReview.objects.first()
    print(f"   Review: {r.rating} stars by {r.user.username}")

if Wishlist.objects.exists():
    w = Wishlist.objects.first()
    print(f"   Wishlist: {w.user.username} -> {w.product.name}")

# 4. Relationships
print("\n4. FOREIGN KEY RELATIONSHIPS:")
if Product.objects.exists():
    p = Product.objects.first()
    print(f"   Product has {p.reviews.count()} reviews")

if Order.objects.exists():
    o = Order.objects.first()
    print(f"   Order has {o.orderitem_set.count()} items")

# 5. Data Types
print("\n5. DATA TYPE VALIDATION:")
if Product.objects.exists():
    p = Product.objects.first()
    print(f"   name: {type(p.name).__name__}")
    print(f"   price: {type(p.price).__name__}")
    print(f"   stock: {type(p.stock).__name__}")
    print(f"   digital: {type(p.digital).__name__}")

# 6. Indexes
print("\n6. DATABASE INDEXES:")
with connection.cursor() as cursor:
    cursor.execute("SHOW INDEX FROM store_product")
    print(f"   store_product: {len(cursor.fetchall())} indexes")
    cursor.execute("SHOW INDEX FROM store_productreview")
    print(f"   store_productreview: {len(cursor.fetchall())} indexes")

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)

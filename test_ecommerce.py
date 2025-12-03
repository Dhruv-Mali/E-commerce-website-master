"""
Quick test script to verify e-commerce functionality
Run: python test_ecommerce.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from apps.store.models import Product, Customer, Order, OrderItem
from django.contrib.auth.models import User

def test_database():
    """Test database connection"""
    print("[+] Testing database connection...")
    try:
        product_count = Product.objects.count()
        print(f"  [OK] Database connected! Found {product_count} products")
        return True
    except Exception as e:
        print(f"  [ERROR] Database error: {e}")
        return False

def test_products():
    """Test product functionality"""
    print("\n[+] Testing products...")
    try:
        products = Product.objects.all()[:5]
        if products:
            for p in products:
                print(f"  [OK] {p.name} - Rs.{p.price} (Stock: {p.stock})")
            return True
        else:
            print("  [WARN] No products found. Add products via admin or populate script.")
            return False
    except Exception as e:
        print(f"  [ERROR] Product error: {e}")
        return False

def test_stripe_config():
    """Test Stripe configuration"""
    print("\n[+] Testing Stripe configuration...")
    from django.conf import settings
    
    if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY:
        if 'your_stripe' in settings.STRIPE_SECRET_KEY:
            print("  [WARN] Stripe keys are placeholders. Update .env with real keys.")
            return False
        else:
            print(f"  [OK] Stripe configured (Key: {settings.STRIPE_SECRET_KEY[:20]}...)")
            return True
    else:
        print("  [ERROR] Stripe keys not configured")
        return False

def test_users():
    """Test user functionality"""
    print("\n[+] Testing users...")
    try:
        user_count = User.objects.count()
        customer_count = Customer.objects.count()
        print(f"  [OK] Found {user_count} users and {customer_count} customers")
        return True
    except Exception as e:
        print(f"  [ERROR] User error: {e}")
        return False

def test_orders():
    """Test order functionality"""
    print("\n[+] Testing orders...")
    try:
        order_count = Order.objects.filter(complete=True).count()
        pending_count = Order.objects.filter(complete=False).count()
        print(f"  [OK] Found {order_count} completed orders, {pending_count} pending")
        return True
    except Exception as e:
        print(f"  [ERROR] Order error: {e}")
        return False

def main():
    print("=" * 60)
    print("E-COMMERCE FUNCTIONALITY TEST")
    print("=" * 60)
    
    results = []
    results.append(("Database", test_database()))
    results.append(("Products", test_products()))
    results.append(("Stripe", test_stripe_config()))
    results.append(("Users", test_users()))
    results.append(("Orders", test_orders()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{name:20} {status}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\nPassed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n[SUCCESS] All tests passed! Your e-commerce site is ready!")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Test checkout with card: 4242 4242 4242 4242")
    else:
        print("\n[WARNING] Some tests failed. Check the errors above.")
        print("See COMPLETE_SETUP_GUIDE.md for troubleshooting.")

if __name__ == "__main__":
    main()

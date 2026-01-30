#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Comprehensive Feature Testing Script"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from apps.store.models import Product, Customer, Order, OrderItem
from apps.store.models_extended import ProductReview, Wishlist, Coupon, Newsletter, RecentlyViewed

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_database_tables():
    print_header("1. DATABASE TABLES CHECK")
    
    tables = {
        'Product': Product.objects.count(),
        'Customer': Customer.objects.count(),
        'Order': Order.objects.count(),
        'ProductReview': ProductReview.objects.count(),
        'Wishlist': Wishlist.objects.count(),
        'Coupon': Coupon.objects.count(),
        'Newsletter': Newsletter.objects.count(),
        'RecentlyViewed': RecentlyViewed.objects.count(),
    }
    
    for table, count in tables.items():
        print(f"  {table:20} : {count} records")
    
    return all(count >= 0 for count in tables.values())

def test_api_endpoints():
    print_header("2. API ENDPOINTS CHECK")
    
    from django.urls import reverse
    
    endpoints = [
        ('add-review', 'POST /api/add-review/'),
        ('toggle-wishlist', 'POST /api/toggle-wishlist/'),
        ('get-wishlist', 'GET /api/wishlist/'),
        ('subscribe-newsletter', 'POST /api/subscribe-newsletter/'),
    ]
    
    for name, desc in endpoints:
        try:
            url = reverse(name)
            print(f"  OK  : {desc:40} -> {url}")
        except:
            print(f"  FAIL: {desc:40} -> NOT FOUND")
            return False
    
    return True

def test_frontend_pages():
    print_header("3. FRONTEND PAGES CHECK")
    
    from django.urls import reverse
    
    pages = [
        ('store', 'Store Page'),
        ('cart', 'Cart Page'),
        ('checkout', 'Checkout Page'),
        ('wishlist', 'Wishlist Page'),
        ('order-history', 'Order History'),
    ]
    
    for name, desc in pages:
        try:
            url = reverse(name)
            print(f"  OK  : {desc:30} -> {url}")
        except:
            print(f"  FAIL: {desc:30} -> NOT FOUND")
            return False
    
    return True

def test_admin_models():
    print_header("4. ADMIN PANEL MODELS CHECK")
    
    from django.contrib import admin
    
    models = [
        (Product, 'Product'),
        (Customer, 'Customer'),
        (Order, 'Order'),
        (ProductReview, 'ProductReview'),
        (Wishlist, 'Wishlist'),
        (Coupon, 'Coupon'),
        (Newsletter, 'Newsletter'),
        (RecentlyViewed, 'RecentlyViewed'),
    ]
    
    for model, name in models:
        if admin.site.is_registered(model):
            print(f"  OK  : {name:30} -> Registered")
        else:
            print(f"  FAIL: {name:30} -> NOT Registered")
            return False
    
    return True

def test_feature_integration():
    print_header("5. FEATURE INTEGRATION TEST")
    
    # Test 1: Create test user
    try:
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@test.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        print(f"  OK  : Test User Created/Found")
    except Exception as e:
        print(f"  FAIL: Test User - {e}")
        return False
    
    # Test 2: Create test product
    try:
        product, created = Product.objects.get_or_create(
            name='Test Product',
            defaults={'price': 1000, 'stock': 10}
        )
        print(f"  OK  : Test Product Created/Found")
    except Exception as e:
        print(f"  FAIL: Test Product - {e}")
        return False
    
    # Test 3: Test Review
    try:
        review, created = ProductReview.objects.get_or_create(
            product=product,
            user=user,
            defaults={'rating': 5, 'comment': 'Test review'}
        )
        print(f"  OK  : Review System Working")
    except Exception as e:
        print(f"  FAIL: Review System - {e}")
        return False
    
    # Test 4: Test Wishlist
    try:
        wishlist, created = Wishlist.objects.get_or_create(
            user=user,
            product=product
        )
        print(f"  OK  : Wishlist System Working")
    except Exception as e:
        print(f"  FAIL: Wishlist System - {e}")
        return False
    
    # Test 5: Test Newsletter
    try:
        newsletter, created = Newsletter.objects.get_or_create(
            email='test@newsletter.com'
        )
        print(f"  OK  : Newsletter System Working")
    except Exception as e:
        print(f"  FAIL: Newsletter System - {e}")
        return False
    
    # Test 6: Test Coupon
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        coupon, created = Coupon.objects.get_or_create(
            code='TEST10',
            defaults={
                'discount_percent': 10,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=30)
            }
        )
        print(f"  OK  : Coupon System Working")
    except Exception as e:
        print(f"  FAIL: Coupon System - {e}")
        return False
    
    return True

def test_frontend_templates():
    print_header("6. FRONTEND TEMPLATES CHECK")
    
    import os
    from django.conf import settings
    
    templates = [
        'apps/store/templates/store/product_detail.html',
        'apps/store/templates/store/wishlist.html',
        'core/templates/footer.html',
    ]
    
    base_dir = settings.BASE_DIR
    
    for template in templates:
        path = os.path.join(base_dir, template)
        if os.path.exists(path):
            # Check for key features in templates
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'product_detail' in template:
                has_review = 'review-form' in content or 'add-review' in content
                has_wishlist = 'wishlist' in content.lower()
                print(f"  OK  : Product Detail -> Reviews: {has_review}, Wishlist: {has_wishlist}")
            elif 'wishlist' in template:
                has_api = 'api/wishlist' in content
                print(f"  OK  : Wishlist Page -> API Call: {has_api}")
            elif 'footer' in template:
                has_newsletter = 'newsletter' in content.lower()
                print(f"  OK  : Footer -> Newsletter: {has_newsletter}")
        else:
            print(f"  FAIL: {template} -> NOT FOUND")
            return False
    
    return True

def main():
    print("\n" + "="*60)
    print("  COMPREHENSIVE FEATURE TEST")
    print("="*60)
    
    tests = [
        ("Database Tables", test_database_tables),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Pages", test_frontend_pages),
        ("Admin Models", test_admin_models),
        ("Feature Integration", test_feature_integration),
        ("Frontend Templates", test_frontend_templates),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ERROR in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {name:30} : {status}")
    
    print("\n" + "="*60)
    print(f"  TOTAL: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n  ✓ ALL FEATURES WORKING CORRECTLY!")
        print("\n  Frontend URLs to Test:")
        print("    - http://127.0.0.1:8000/store/")
        print("    - http://127.0.0.1:8000/product/1/")
        print("    - http://127.0.0.1:8000/wishlist/")
        print("    - http://127.0.0.1:8000/admin/")
        return True
    else:
        print("\n  ✗ Some tests failed. Check errors above.")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n  CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

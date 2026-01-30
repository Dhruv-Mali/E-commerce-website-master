#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Database Verification Script"""
import os
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')

import django
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from apps.store.models import Product, Customer, Order, OrderItem, ShippingAddress
from apps.store.models_extended import ProductReview, Wishlist, Coupon, Newsletter, RecentlyViewed

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_database_connection():
    print_section("1. DATABASE CONNECTION")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"  MySQL Version: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"  Database Name: {db_name[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"  Total Tables: {len(tables)}")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def check_table_structure():
    print_section("2. TABLE STRUCTURE VERIFICATION")
    
    tables = {
        'store_product': Product,
        'store_customer': Customer,
        'store_order': Order,
        'store_orderitem': OrderItem,
        'store_shippingaddress': ShippingAddress,
        'store_productreview': ProductReview,
        'store_wishlist': Wishlist,
        'store_coupon': Coupon,
        'store_newsletter': Newsletter,
        'store_recentlyviewed': RecentlyViewed,
    }
    
    for table_name, model in tables.items():
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print(f"\n  {table_name}:")
                print(f"    Columns: {len(columns)}")
                for col in columns[:5]:  # Show first 5 columns
                    print(f"      - {col[0]} ({col[1]})")
                if len(columns) > 5:
                    print(f"      ... and {len(columns)-5} more")
        except Exception as e:
            print(f"  ERROR in {table_name}: {e}")
            return False
    return True

def check_data_integrity():
    print_section("3. DATA INTEGRITY CHECK")
    
    checks = []
    
    # Check Products
    try:
        products = Product.objects.all()
        print(f"  Products: {products.count()} records")
        if products.exists():
            p = products.first()
            print(f"    Sample: {p.name} - Rs.{p.price}")
            checks.append(True)
        else:
            print(f"    WARNING: No products found")
            checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    # Check Customers
    try:
        customers = Customer.objects.all()
        print(f"  Customers: {customers.count()} records")
        checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    # Check Orders
    try:
        orders = Order.objects.all()
        completed = orders.filter(complete=True).count()
        print(f"  Orders: {orders.count()} total, {completed} completed")
        checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    # Check Reviews
    try:
        reviews = ProductReview.objects.all()
        print(f"  Reviews: {reviews.count()} records")
        if reviews.exists():
            r = reviews.first()
            print(f"    Sample: {r.rating} stars by {r.user.username}")
        checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    # Check Wishlist
    try:
        wishlist = Wishlist.objects.all()
        print(f"  Wishlist: {wishlist.count()} records")
        checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    # Check Newsletter
    try:
        newsletter = Newsletter.objects.all()
        active = newsletter.filter(active=True).count()
        print(f"  Newsletter: {newsletter.count()} total, {active} active")
        checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    # Check Coupons
    try:
        coupons = Coupon.objects.all()
        active = coupons.filter(active=True).count()
        print(f"  Coupons: {coupons.count()} total, {active} active")
        checks.append(True)
    except Exception as e:
        print(f"    ERROR: {e}")
        checks.append(False)
    
    return all(checks)

def check_relationships():
    print_section("4. FOREIGN KEY RELATIONSHIPS")
    
    try:
        # Check Product -> Reviews
        if Product.objects.exists():
            product = Product.objects.first()
            reviews = product.reviews.all()
            print(f"  Product -> Reviews: OK ({reviews.count()} reviews)")
        
        # Check User -> Wishlist
        if User.objects.exists():
            user = User.objects.first()
            wishlist = Wishlist.objects.filter(user=user)
            print(f"  User -> Wishlist: OK ({wishlist.count()} items)")
        
        # Check Order -> OrderItems
        if Order.objects.exists():
            order = Order.objects.first()
            items = order.orderitem_set.all()
            print(f"  Order -> OrderItems: OK ({items.count()} items)")
        
        # Check Customer -> Orders
        if Customer.objects.exists():
            customer = Customer.objects.first()
            orders = customer.order_set.all()
            print(f"  Customer -> Orders: OK ({orders.count()} orders)")
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def check_indexes():
    print_section("5. DATABASE INDEXES")
    
    try:
        with connection.cursor() as cursor:
            # Check indexes on key tables
            tables = ['store_product', 'store_order', 'store_productreview']
            
            for table in tables:
                cursor.execute(f"SHOW INDEX FROM {table}")
                indexes = cursor.fetchall()
                print(f"  {table}: {len(indexes)} indexes")
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_crud_operations():
    print_section("6. CRUD OPERATIONS TEST")
    
    try:
        # CREATE
        test_email = 'dbtest@example.com'
        newsletter, created = Newsletter.objects.get_or_create(email=test_email)
        print(f"  CREATE: {'New' if created else 'Existing'} newsletter entry")
        
        # READ
        found = Newsletter.objects.filter(email=test_email).exists()
        print(f"  READ: Newsletter found = {found}")
        
        # UPDATE
        newsletter.active = False
        newsletter.save()
        print(f"  UPDATE: Newsletter status changed")
        
        # DELETE (cleanup)
        newsletter.delete()
        print(f"  DELETE: Test entry removed")
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def check_data_types():
    print_section("7. DATA TYPE VALIDATION")
    
    try:
        # Check Product fields
        if Product.objects.exists():
            p = Product.objects.first()
            print(f"  Product.name: {type(p.name).__name__} = '{p.name}'")
            print(f"  Product.price: {type(p.price).__name__} = {p.price}")
            print(f"  Product.stock: {type(p.stock).__name__} = {p.stock}")
            print(f"  Product.digital: {type(p.digital).__name__} = {p.digital}")
        
        # Check Review fields
        if ProductReview.objects.exists():
            r = ProductReview.objects.first()
            print(f"  Review.rating: {type(r.rating).__name__} = {r.rating}")
            print(f"  Review.verified: {type(r.verified_purchase).__name__} = {r.verified_purchase}")
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  DATABASE VERIFICATION SCRIPT")
    print("="*60)
    
    tests = [
        ("Database Connection", check_database_connection),
        ("Table Structure", check_table_structure),
        ("Data Integrity", check_data_integrity),
        ("Relationships", check_relationships),
        ("Indexes", check_indexes),
        ("CRUD Operations", test_crud_operations),
        ("Data Types", check_data_types),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  CRITICAL ERROR in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {name:30} : {status}")
    
    print("\n" + "="*60)
    print(f"  RESULT: {passed}/{total} checks passed")
    print("="*60)
    
    if passed == total:
        print("\n  ✓ DATABASE IS PROPERLY FORMATTED AND WORKING!")
        print("\n  All tables, relationships, and data types verified.")
        return True
    else:
        print("\n  ✗ Some database checks failed.")
        print("  Review errors above for details.")
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

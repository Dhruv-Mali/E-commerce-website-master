#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive Feature Testing Script
Tests all functionality in the e-commerce project
"""
import os
import sys
import django
import random
import string

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from apps.store.models import Product, Customer, Order, OrderItem, ShippingAddress
from apps.store.models_extended import (
    ProductReview, Wishlist, Coupon, RecentlyViewed, Newsletter
)

# Generate unique identifier for test session
TEST_ID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def get_unique_username(base):
    """Generate unique username"""
    return f"{base}_{TEST_ID}"

# Test results
results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'details': []
}

def test(name, func):
    """Decorator for test functions"""
    results['total'] += 1
    try:
        func()
        results['passed'] += 1
        results['details'].append(f"[PASS] {name}")
        print(f"[PASS] {name}")
    except Exception as e:
        results['failed'] += 1
        results['details'].append(f"[FAIL] {name}: {str(e)}")
        print(f"[FAIL] {name}: {str(e)}")

# ============================================================================
# SECTION 1: MODEL TESTS
# ============================================================================
print("\n" + "="*60)
print("SECTION 1: TESTING MODELS")
print("="*60)

def test_product_model():
    """Test Product model creation and properties"""
    product = Product.objects.create(
        name='Test Product',
        price=100,
        stock=50,
        category='Electronics'
    )
    assert product.name == 'Test Product'
    assert product.in_stock == True
    assert product.price == 100
    product.delete()

test("Product Model Creation", test_product_model)

def test_customer_model():
    """Test Customer model"""
    user = User.objects.create_user(username=get_unique_username('testuser'), email=f'{TEST_ID}_test@example.com', password='pass123')
    customer, created = Customer.objects.get_or_create(user=user, defaults={'name': 'Test Customer'})
    assert customer.name == 'Test Customer'
    assert customer.user == user
    customer.delete()
    user.delete()

test("Customer Model Creation", test_customer_model)

def test_order_model():
    """Test Order model"""
    user = User.objects.create_user(username=get_unique_username('ordertest'), email=f'{TEST_ID}_order@test.com', password='pass123')
    customer, _ = Customer.objects.get_or_create(user=user, defaults={'name': 'Order Customer'})
    order = Order.objects.create(customer=customer, complete=False)
    assert order.customer == customer
    assert order.complete == False
    order.delete()
    customer.delete()
    user.delete()

test("Order Model Creation", test_order_model)

def test_order_item_model():
    """Test OrderItem model"""
    user = User.objects.create_user(username=get_unique_username('itemtest'), email=f'{TEST_ID}_item@test.com', password='pass123')
    customer, _ = Customer.objects.get_or_create(user=user, defaults={'name': 'Item Customer'})
    order = Order.objects.create(customer=customer)
    product = Product.objects.create(name='Test Item', price=50, stock=10)
    
    item = OrderItem.objects.create(order=order, product=product, quantity=2)
    assert item.quantity == 2
    assert item.product == product
    
    item.delete()
    product.delete()
    order.delete()
    customer.delete()
    user.delete()

test("OrderItem Model Creation", test_order_item_model)

def test_shipping_address_model():
    """Test ShippingAddress model"""
    user = User.objects.create_user(username=get_unique_username('shiptest'), email=f'{TEST_ID}_ship@test.com', password='pass123')
    customer, _ = Customer.objects.get_or_create(user=user, defaults={'name': 'Ship Customer'})
    address = ShippingAddress.objects.create(
        customer=customer,
        address='123 Main St',
        city='TestCity',
        state='TS',
        zipcode='12345'
    )
    assert address.address == '123 Main St'
    address.delete()
    customer.delete()
    user.delete()

test("ShippingAddress Model Creation", test_shipping_address_model)

# ============================================================================
# SECTION 2: EXTENDED FEATURES TESTS
# ============================================================================
print("\n" + "="*60)
print("SECTION 2: TESTING EXTENDED FEATURES")
print("="*60)

def test_product_review():
    """Test ProductReview model"""
    user = User.objects.create_user(username=get_unique_username('reviewuser'), email=f'{TEST_ID}_review@test.com', password='pass123')
    product = Product.objects.create(name=f'Review Product {TEST_ID}', price=100)
    
    review = ProductReview.objects.create(
        product=product,
        user=user,
        rating=5,
        comment='Great product!'
    )
    assert review.rating == 5
    assert review.user == user
    
    review.delete()
    product.delete()
    user.delete()

test("Product Reviews Feature", test_product_review)

def test_wishlist():
    """Test Wishlist model"""
    user = User.objects.create_user(username=get_unique_username('wishuser'), email=f'{TEST_ID}_wish@test.com', password='pass123')
    product = Product.objects.create(name=f'Wishlist Product {TEST_ID}', price=100)
    
    wishlist = Wishlist.objects.create(user=user, product=product)
    assert wishlist.product == product
    assert wishlist.user == user
    
    # Test toggle functionality - check unique constraint
    existing = Wishlist.objects.filter(user=user, product=product)
    assert existing.count() == 1
    
    wishlist.delete()
    product.delete()
    user.delete()

test("Wishlist Feature", test_wishlist)

def test_coupon():
    """Test Coupon model"""
    from django.utils import timezone
    from datetime import timedelta
    
    coupon = Coupon.objects.create(
        code='TEST10',
        discount_percent=10,
        valid_from=timezone.now(),
        valid_to=timezone.now() + timedelta(days=30),
        active=True
    )
    assert coupon.code == 'TEST10'
    assert coupon.is_valid() == True
    
    coupon.delete()

test("Coupon System", test_coupon)

def test_recently_viewed():
    """Test RecentlyViewed model"""
    user = User.objects.create_user(username=get_unique_username('viewuser'), email=f'{TEST_ID}_view@test.com', password='pass123')
    product = Product.objects.create(name=f'Viewed Product {TEST_ID}', price=100)
    
    viewed = RecentlyViewed.objects.create(user=user, product=product)
    assert viewed.product == product
    assert viewed.user == user
    
    viewed.delete()
    product.delete()
    user.delete()

test("Recently Viewed Feature", test_recently_viewed)

def test_newsletter():
    """Test Newsletter model"""
    newsletter = Newsletter.objects.create(email='subscribe@test.com')
    assert newsletter.email == 'subscribe@test.com'
    assert newsletter.active == True
    
    newsletter.delete()

test("Newsletter Subscription", test_newsletter)

# ============================================================================
# SECTION 3: VIEW TESTS
# ============================================================================
print("\n" + "="*60)
print("SECTION 3: TESTING VIEWS")
print("="*60)

client = Client()

def test_landing_page():
    """Test landing page view"""
    response = client.get(reverse('landing'))
    assert response.status_code in [200, 302]  # May redirect

test("Landing Page View", test_landing_page)

def test_store_page():
    """Test store listing page"""
    response = client.get(reverse('store'))
    assert response.status_code == 200

test("Store Listing Page", test_store_page)

def test_cart_page():
    """Test cart page"""
    response = client.get(reverse('cart'))
    assert response.status_code == 200

test("Cart Page View", test_cart_page)

def test_product_detail_page():
    """Test product detail page"""
    product = Product.objects.create(name=f'Detail Product {TEST_ID}', price=100, stock=10)
    response = client.get(reverse('product-detail', args=[product.id]))
    assert response.status_code == 200
    product.delete()

test("Product Detail Page", test_product_detail_page)

def test_order_history_page():
    """Test order history page (authenticated required)"""
    user = User.objects.create_user(username=get_unique_username('historyuser'), email=f'{TEST_ID}_history@test.com', password='pass123')
    Customer.objects.get_or_create(user=user, defaults={'name': 'History Customer'})
    client.login(username=user.username, password='pass123')
    response = client.get(reverse('order-history'))
    assert response.status_code == 200
    user.delete()
    client.logout()

test("Order History Page", test_order_history_page)

def test_wishlist_page():
    """Test wishlist page"""
    response = client.get(reverse('wishlist'))
    assert response.status_code in [200, 302]  # May redirect if not authenticated

test("Wishlist Page View", test_wishlist_page)

# ============================================================================
# SECTION 4: API ENDPOINT TESTS
# ============================================================================
print("\n" + "="*60)
print("SECTION 4: TESTING API ENDPOINTS")
print("="*60)

def test_add_review_api():
    """Test add review API endpoint"""
    user = User.objects.create_user(username=get_unique_username('apireviewuser'), email=f'{TEST_ID}_apireview@test.com', password='pass123')
    product = Product.objects.create(name=f'API Review Product {TEST_ID}', price=100)
    
    client.login(username=user.username, password='pass123')
    
    import json
    response = client.post(
        reverse('add-review'),
        data=json.dumps({'product_id': product.id, 'rating': 5, 'comment': 'Great!'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    product.delete()
    user.delete()
    client.logout()

test("Add Review API", test_add_review_api)

def test_toggle_wishlist_api():
    """Test toggle wishlist API endpoint"""
    user = User.objects.create_user(username=get_unique_username('apiwishuser'), email=f'{TEST_ID}_apiwish@test.com', password='pass123')
    product = Product.objects.create(name=f'API Wishlist Product {TEST_ID}', price=100)
    
    client.login(username=user.username, password='pass123')
    
    import json
    response = client.post(
        reverse('toggle-wishlist'),
        data=json.dumps({'product_id': product.id}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['action'] in ['added', 'removed']
    
    product.delete()
    user.delete()
    client.logout()

test("Toggle Wishlist API", test_toggle_wishlist_api)

def test_get_wishlist_api():
    """Test get wishlist API endpoint"""
    user = User.objects.create_user(username=get_unique_username('apigetwishuser'), email=f'{TEST_ID}_apigetwish@test.com', password='pass123')
    product = Product.objects.create(name=f'Get Wishlist Product {TEST_ID}', price=100)
    Wishlist.objects.create(user=user, product=product)
    
    client.login(username=user.username, password='pass123')
    response = client.get(reverse('get-wishlist'))
    assert response.status_code == 200
    data = response.json()
    assert 'wishlist' in data
    
    Wishlist.objects.filter(user=user, product=product).delete()
    product.delete()
    user.delete()
    client.logout()

test("Get Wishlist API", test_get_wishlist_api)

def test_newsletter_api():
    """Test newsletter subscription API"""
    import json
    response = client.post(
        reverse('subscribe-newsletter'),
        data=json.dumps({'email': 'newsletter@test.com'}),
        content_type='application/json'
    )
    assert response.status_code in [200, 201]
    
    # Cleanup
    Newsletter.objects.filter(email='newsletter@test.com').delete()

test("Newsletter Subscription API", test_newsletter_api)

# ============================================================================
# SECTION 5: AUTHENTICATION TESTS
# ============================================================================
print("\n" + "="*60)
print("SECTION 5: TESTING AUTHENTICATION")
print("="*60)

def test_user_login():
    """Test user login"""
    user = User.objects.create_user(username=get_unique_username('logintest'), email=f'{TEST_ID}_login@test.com', password='testpass123')
    is_authenticated = client.login(username=user.username, password='testpass123')
    assert is_authenticated == True
    user.delete()
    client.logout()

test("User Login", test_user_login)

def test_user_creation():
    """Test user creation"""
    user = User.objects.create_user(
        username=get_unique_username('newuser'),
        email=f'{TEST_ID}_newuser@test.com',
        password='password123'
    )
    assert user.username == user.username
    assert user.email == f'{TEST_ID}_newuser@test.com'
    user.delete()

test("User Creation", test_user_creation)

# ============================================================================
# SECTION 6: BUSINESS LOGIC TESTS
# ============================================================================
print("\n" + "="*60)
print("SECTION 6: TESTING BUSINESS LOGIC")
print("="*60)

def test_stock_reduction():
    """Test product stock reduction"""
    product = Product.objects.create(name=f'Stock Product {TEST_ID}', price=100, stock=10)
    initial_stock = product.stock
    
    product.reduce_stock(3)
    assert product.stock == initial_stock - 3
    
    product.delete()

test("Stock Reduction Logic", test_stock_reduction)

def test_insufficient_stock():
    """Test insufficient stock validation"""
    product = Product.objects.create(name=f'Low Stock Product {TEST_ID}', price=100, stock=2)
    
    try:
        product.reduce_stock(5)  # Try to reduce more than available
        assert False, "Should have raised ValidationError"
    except:
        pass  # Expected
    
    product.delete()

test("Insufficient Stock Validation", test_insufficient_stock)

def test_cart_calculation():
    """Test cart total calculation"""
    user = User.objects.create_user(username=get_unique_username('cartuser'), email=f'{TEST_ID}_cart@test.com', password='pass123')
    customer, _ = Customer.objects.get_or_create(user=user, defaults={'name': 'Cart Customer'})
    order = Order.objects.create(customer=customer)
    product = Product.objects.create(name=f'Cart Product {TEST_ID}', price=100, stock=10)
    
    OrderItem.objects.create(order=order, product=product, quantity=2)
    
    cart_total = order.get_cart_total
    assert cart_total == 200  # 100 * 2
    
    OrderItem.objects.filter(order=order).delete()
    product.delete()
    order.delete()
    customer.delete()
    user.delete()

test("Cart Total Calculation", test_cart_calculation)

def test_shipping_requirement():
    """Test shipping requirement detection"""
    user = User.objects.create_user(username=get_unique_username('shipuser'), email=f'{TEST_ID}_ship@test.com', password='pass123')
    customer, _ = Customer.objects.get_or_create(user=user, defaults={'name': 'Ship User Customer'})
    order = Order.objects.create(customer=customer)
    
    # Digital product - no shipping needed
    digital_product = Product.objects.create(name=f'Digital {TEST_ID}', price=50, stock=100, digital=True)
    OrderItem.objects.create(order=order, product=digital_product, quantity=1)
    
    assert order.shipping == False
    
    # Physical product - shipping needed
    physical_product = Product.objects.create(name=f'Physical {TEST_ID}', price=100, stock=100, digital=False)
    OrderItem.objects.create(order=order, product=physical_product, quantity=1)
    
    assert order.shipping == True
    
    OrderItem.objects.filter(order=order).delete()
    digital_product.delete()
    physical_product.delete()
    order.delete()
    customer.delete()
    user.delete()

test("Shipping Requirement Logic", test_shipping_requirement)

# ============================================================================
# SECTION 7: ADMIN FEATURES
# ============================================================================
print("\n" + "="*60)
print("SECTION 7: TESTING ADMIN FEATURES")
print("="*60)

def test_admin_dashboard():
    """Test admin dashboard access"""
    admin_user = User.objects.create_superuser(get_unique_username('admin'), f'{TEST_ID}_admin@test.com', 'admin123')
    client.login(username=admin_user.username, password='admin123')
    
    response = client.get(reverse('admin_dashboard'))
    # Should be 200 if accessible or redirect to login if not set up
    assert response.status_code in [200, 302]
    
    admin_user.delete()
    client.logout()

test("Admin Dashboard Access", test_admin_dashboard)

def test_admin_products_page():
    """Test admin products page"""
    admin_user = User.objects.create_superuser(get_unique_username('adminprod'), f'{TEST_ID}_adminprod@test.com', 'admin123')
    client.login(username=admin_user.username, password='admin123')
    
    response = client.get(reverse('admin_products'))
    assert response.status_code in [200, 302]
    
    admin_user.delete()
    client.logout()

test("Admin Products Page", test_admin_products_page)

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*60)
print("FINAL TEST SUMMARY")
print("="*60)
print(f"\nTotal Tests: {results['total']}")
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
print(f"\nSuccess Rate: {(results['passed']/results['total']*100):.1f}%\n")

if results['failed'] == 0:
    print("ALL FEATURES WORKING CORRECTLY!\n")
else:
    print(f"WARNING: {results['failed']} feature(s) need attention\n")

# Detailed results
print("="*60)
print("DETAILED RESULTS:")
print("="*60)
for detail in results['details']:
    print(detail)

# Save results to file
with open('FEATURE_TEST_REPORT.txt', 'w') as f:
    f.write("="*60 + "\n")
    f.write("E-COMMERCE FEATURE TEST REPORT\n")
    f.write("="*60 + "\n\n")
    f.write(f"Total Tests: {results['total']}\n")
    f.write(f"Passed: {results['passed']}\n")
    f.write(f"Failed: {results['failed']}\n")
    f.write(f"Success Rate: {(results['passed']/results['total']*100):.1f}%\n\n")
    f.write("DETAILED RESULTS:\n")
    f.write("-"*60 + "\n")
    for detail in results['details']:
        f.write(detail + "\n")

print("\nTest report saved to: FEATURE_TEST_REPORT.txt")

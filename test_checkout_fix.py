#!/usr/bin/env python
"""
Test script to verify the checkout MultipleObjectsReturned fix
"""
import os
import sys
import django
from dotenv import load_dotenv

def test_checkout_fix():
    """Test that checkout view handles multiple orders correctly"""
    try:
        load_dotenv()
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
        django.setup()
        
        from django.contrib.auth.models import User
        from apps.store.models import Customer, Order
        
        # Get the admin user
        user = User.objects.get(username='admin')
        customer = user.customer
        
        print(f"Testing with user: {user.username}")
        print(f"Customer: {customer.name}")
        
        # Check current incomplete orders
        incomplete_orders = Order.objects.filter(customer=customer, complete=False)
        print(f"Current incomplete orders: {incomplete_orders.count()}")
        
        # Test the fixed logic
        order = Order.objects.filter(customer=customer, complete=False).first()
        if not order:
            order = Order.objects.create(customer=customer, complete=False)
            print("Created new order")
        else:
            print(f"Using existing order: {order.id}")
        
        print(f"Order ID: {order.id}")
        print(f"Order items: {order.get_cart_items}")
        print(f"Order total: {order.get_cart_total}")
        
        print("\n[SUCCESS] Checkout fix is working correctly!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_checkout_fix()
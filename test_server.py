#!/usr/bin/env python
"""
Test script to check if Django server can start without errors
"""
import os
import sys
import django
from dotenv import load_dotenv

def test_django_setup():
    """Test Django configuration and imports"""
    try:
        load_dotenv()
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
        django.setup()
        
        print("[OK] Django setup successful")
        
        # Test database connection
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("[OK] Database connection successful")
        
        # Test model imports
        from apps.store.models import Product, Customer, Order
        print("[OK] Model imports successful")
        
        # Test views imports
        from apps.store.views import store, cart, checkout
        print("[OK] View imports successful")
        
        # Test URL configuration
        from django.urls import reverse
        store_url = reverse('store')
        print(f"[OK] URL routing successful: {store_url}")
        
        # Test template loading
        from django.template.loader import get_template
        template = get_template('index.html')
        print("[OK] Template loading successful")
        
        print("\n[SUCCESS] All tests passed! Server should start without errors.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_django_setup()
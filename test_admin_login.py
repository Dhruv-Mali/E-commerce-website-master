#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def test_admin_login():
    print("=" * 60)
    print("TESTING ADMIN LOGIN")
    print("=" * 60)
    
    # Test credentials
    username = 'admin'
    password = 'admin123'
    
    # Try to authenticate
    user = authenticate(username=username, password=password)
    
    if user is not None:
        print("LOGIN SUCCESSFUL!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Active: {user.is_active}")
        print(f"Email: {user.email}")
        print("")
        print("ACCESS URLS:")
        print("Admin Panel: http://127.0.0.1:8000/admin/")
        print("Main Site: http://127.0.0.1:8000/")
        print("Login Page: http://127.0.0.1:8000/login/")
    else:
        print("LOGIN FAILED!")
        print("Checking user status...")
        
        try:
            user = User.objects.get(username=username)
            print(f"User exists: {user.username}")
            print(f"Is Active: {user.is_active}")
            print(f"Is Superuser: {user.is_superuser}")
            print("Password might be incorrect.")
        except User.DoesNotExist:
            print("User does not exist!")
    
    print("=" * 60)

if __name__ == "__main__":
    test_admin_login()
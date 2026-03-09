#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.contrib.auth.models import User

def reset_admin_password():
    try:
        # Get the main admin user
        admin_user = User.objects.get(username='admin')
        
        # Set new password
        new_password = 'admin123'
        admin_user.set_password(new_password)
        admin_user.save()
        
        print("=" * 50)
        print("ADMIN PASSWORD RESET SUCCESSFUL!")
        print("=" * 50)
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"New Password: {new_password}")
        print(f"Admin URL: http://127.0.0.1:8000/admin/")
        print("=" * 50)
        
    except User.DoesNotExist:
        print("Admin user not found. Creating new admin user...")
        
        # Create new admin user
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        print("=" * 50)
        print("NEW ADMIN USER CREATED!")
        print("=" * 50)
        print(f"Username: admin")
        print(f"Email: admin@example.com")
        print(f"Password: admin123")
        print(f"Admin URL: http://127.0.0.1:8000/admin/")
        print("=" * 50)

if __name__ == "__main__":
    reset_admin_password()
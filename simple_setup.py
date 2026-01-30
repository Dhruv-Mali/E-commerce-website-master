#!/usr/bin/env python
"""Simple database setup script"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("DATABASE SETUP")
    print("=" * 60)
    
    # Run migrations
    print("\nRunning makemigrations...")
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'])
    
    print("\nRunning migrate...")
    subprocess.run([sys.executable, 'manage.py', 'migrate'])
    
    # Create superuser
    print("\nCreating superuser...")
    subprocess.run(
        [sys.executable, 'manage.py', 'shell'],
        input="""
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
""",
        text=True
    )
    
    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE")
    print("=" * 60)
    print("\nAdmin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nYou can now run: python manage.py runserver 8081")

if __name__ == '__main__':
    main()

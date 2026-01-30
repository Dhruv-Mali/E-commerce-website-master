#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple database setup script"""
import os
import sys
import subprocess

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def run_command(cmd):
    """Run a command and print output"""
    print(f"\n▶ Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    print("=" * 60)
    print("DATABASE SETUP")
    print("=" * 60)
    
    # Run migrations
    if not run_command([sys.executable, 'manage.py', 'makemigrations']):
        print("❌ makemigrations failed")
        return False
    
    if not run_command([sys.executable, 'manage.py', 'migrate']):
        print("❌ migrate failed")
        return False
    
    # Create superuser
    print("\n▶ Creating superuser...")
    result = subprocess.run(
        [sys.executable, 'manage.py', 'shell'],
        input="""
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin / admin123')
else:
    print('✅ Superuser already exists')
""",
        text=True,
        capture_output=True
    )
    print(result.stdout)
    
    print("\n" + "=" * 60)
    print("✅ DATABASE SETUP COMPLETE")
    print("=" * 60)
    print("\nAdmin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

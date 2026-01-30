#!/usr/bin/env python
"""Quick setup script for improvements"""
import os
import sys
import subprocess

def run_command(cmd, description):
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("🚀 E-COMMERCE IMPROVEMENTS SETUP")
    print("="*60)
    
    steps = [
        ("pip install -r requirements.txt", "Installing dependencies"),
        ("python manage.py makemigrations store", "Creating migrations"),
        ("python manage.py migrate", "Running migrations"),
    ]
    
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n❌ Failed: {desc}")
            return False
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\n🎉 New Features:")
    print("   - Product Reviews & Ratings")
    print("   - Wishlist System")
    print("   - Newsletter Subscription")
    print("   - Enhanced Logging")
    print("   - Performance Caching")
    print("\n📝 Run: python manage.py runserver")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

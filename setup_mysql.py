#!/usr/bin/env python
"""
MySQL Database Setup Script for Django E-commerce Project
"""
import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

def create_database():
    """Create MySQL database if it doesn't exist"""
    load_dotenv()
    
    # Get database credentials from environment
    db_name = os.environ.get('DB_NAME', 'ecommerce_db')
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '3306')
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{db_name}' created successfully (or already exists)")
            
            # Grant privileges (optional, for security)
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'{db_host}'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"Privileges granted to user '{db_user}'")
            
            cursor.close()
            connection.close()
            
            return True
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials in .env file are correct")
        print("3. User has permission to create databases")
        return False

def test_django_connection():
    """Test Django database connection"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
        import django
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("Django MySQL connection successful")
            return True
            
    except Exception as e:
        print(f"Django MySQL connection failed: {e}")
        return False

if __name__ == '__main__':
    print("Setting up MySQL database for Django E-commerce...")
    print("=" * 50)
    
    # Step 1: Create database
    if create_database():
        print("\nTesting Django connection...")
        
        # Step 2: Test Django connection
        if test_django_connection():
            print("\nMySQL setup completed successfully!")
            print("\nNext steps:")
            print("1. Update your .env file with correct MySQL password")
            print("2. Run: python manage.py migrate")
            print("3. Run: python manage.py runserver")
        else:
            print("\nDjango connection failed. Please check your settings.")
    else:
        print("\nDatabase creation failed. Please check MySQL connection.")
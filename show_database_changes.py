#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.db import connection

print('✅ DATABASE CHANGES - MySQL Database Structure')
print('=' * 80)

cursor = connection.cursor()

# Get all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

new_tables = ['loginsys_otp', 'loginsys_userphone']

print('\n🆕 NEW TABLES CREATED (OTP Authentication System):')
print('-' * 80)

for table_info in tables:
    table_name = table_info[0]
    
    if table_name in new_tables:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        
        print(f'\n📋 TABLE: {table_name}')
        print('   Columns:')
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            nullable = 'YES' if col[2] == 'YES' else 'NO'
            key = col[3] if col[3] else '-'
            extra = col[5] if col[5] else '-'
            print(f'     • {col_name:25} {col_type:30} (null: {nullable}, key: {key}, extra: {extra})')

print('\n' + '=' * 80)
print('SUMMARY OF CHANGES:')
print('-' * 80)
print('''
✅ 2 New Tables Created:

1. loginsys_otp
   - Stores OTP codes with 6-digit security
   - Tracks phone_number, otp_code, otp_type
   - Includes is_verified, attempts, created_at, expires_at
   - Used for OTP generation and verification

2. loginsys_userphone
   - Links User to Phone Number (OneToOne relationship)
   - Stores phone_number (unique), is_verified
   - Includes created_at, updated_at timestamps
   - Used for OTP delivery and user identification

These tables enable the complete OTP authentication system:
✅ User registration with phone number
✅ OTP code generation and storage
✅ OTP verification and attempt tracking
✅ Phone number management
''')
print('=' * 80)

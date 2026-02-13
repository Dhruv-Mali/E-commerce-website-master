#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.db import connection
from django.apps import apps

print('\n' + '='*90)
print('✅ DATABASE VALIDATION - Complete Table Check')
print('='*90)

# Get database info
db_engine = connection.vendor.upper()
db_name = connection.settings_dict.get('NAME', 'default')

print(f'\n📊 DATABASE INFO:')
print(f'   Engine: {db_engine}')
print(f'   Database: {db_name}')
print(f'   Connection: {connection.settings_dict["ENGINE"]}')

print('\n' + '-'*90)
print('ALL EXISTING TABLES IN DATABASE:')
print('-'*90)

# Get all tables
cursor = connection.cursor()

if db_engine == 'SQLITE':
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
elif db_engine == 'MYSQL':
    cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name}'")
    tables = [row[0] for row in cursor.fetchall()]
else:
    tables = []

# Organize tables by app
apps_tables = {}
for table in sorted(tables):
    if table.startswith('django_'):
        app = 'django_core'
    elif table.startswith('auth_'):
        app = 'auth'
    elif table.startswith('loginsys_'):
        app = 'loginsys (OTP)'
    elif table.startswith('store_'):
        app = 'store'
    else:
        app = 'other'
    
    if app not in apps_tables:
        apps_tables[app] = []
    apps_tables[app].append(table)

print('\n📋 TABLES BY APPLICATION:\n')

for app in sorted(apps_tables.keys()):
    status_emoji = '✅' if 'OTP' not in app else '🆕'
    print(f'{status_emoji} {app.upper()}:')
    for table in sorted(apps_tables[app]):
        if 'OTP' in app and 'otp' in table:
            marker = '🆕 NEW'
        else:
            marker = '✓'
        print(f'     {marker} {table}')
    print()

print('-'*90)
print('✅ OTP SYSTEM SPECIFIC TABLES:')
print('-'*90)

otp_tables = ['loginsys_otp', 'loginsys_userphone']
found_otp = []
missing_otp = []

for table in otp_tables:
    if table in tables:
        found_otp.append(table)
        print(f'✅ {table:30} FOUND')
    else:
        missing_otp.append(table)
        print(f'❌ {table:30} MISSING')

print('\n' + '-'*90)
print('TABLE STRUCTURE & ROW COUNT:')
print('-'*90 + '\n')

# Get table details
for table_name in found_otp:
    print(f'📋 TABLE: {table_name}')
    print('   ' + '-'*86)
    
    # Get columns
    if db_engine == 'SQLITE':
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print('   Columns:')
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            null_info = '(NOT NULL)' if not_null else '(nullable)'
            pk_info = '(PRIMARY KEY)' if pk else ''
            print(f'     • {col_name:25} {col_type:20} {null_info:15} {pk_info}')
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f'   Total Rows: {count}')
    print()

print('-'*90)
print('DJANGO MIGRATIONS STATUS:')
print('-'*90 + '\n')

cursor.execute("SELECT app, name, applied FROM django_migrations WHERE app='loginsys'")
migrations = cursor.fetchall()

if migrations:
    print('✅ OTP MIGRATIONS:')
    for app, name, applied in migrations:
        print(f'   ✓ {name:40} - {applied}')
else:
    print('❌ NO OTP MIGRATIONS FOUND')

print('\n' + '='*90)

# Final status
if len(found_otp) == len(otp_tables):
    print('✅ DATABASE STATUS: ALL TABLES PRESENT AND CORRECT')
else:
    print(f'⚠️  DATABASE STATUS: {len(found_otp)}/{len(otp_tables)} OTP tables found')
    if missing_otp:
        print(f'   Missing: {", ".join(missing_otp)}')
    print('   Action: Run "python manage.py migrate" to create missing tables')

print('='*90 + '\n')

# Summary table
print('📊 SUMMARY TABLE:')
print('-'*90)
print(f'Total Tables in Database: {len(tables)}')
print(f'OTP Tables Found: {len(found_otp)}/{len(otp_tables)}')
print(f'OTP Tables Missing: {len(missing_otp)}/{len(otp_tables)}')
print(f'Database Engine: {db_engine}')
print('-'*90 + '\n')

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.loginsys.otp_models import UserPhone

User = get_user_model()

# Find non-admin users (not staff and not superuser)
non_admin_users = User.objects.filter(is_staff=False, is_superuser=False)
count = non_admin_users.count()

print(f"Found {count} non-admin users. They will be deleted.")
if count == 0:
    print('No non-admin users to delete.')
    exit(0)

print('Listing users to be deleted:')
for u in non_admin_users:
    phone = ''
    try:
        up = UserPhone.objects.get(user=u)
        phone = up.phone_number
    except UserPhone.DoesNotExist:
        phone = ''
    print(f' - ID: {u.id}, username: {u.username}, email: {u.email}, phone: {phone}')

confirm = input('\nType YES to confirm deletion of these users: ')
if confirm != 'YES':
    print('Aborted by user. No changes made.')
    exit(1)

# Perform deletion
ids = list(non_admin_users.values_list('id', flat=True))
print(f'Deleting {len(ids)} users...')

# Deleting users via queryset to cascade related objects
deleted_info = non_admin_users.delete()
print('\nDeletion result (model, count):')
print(deleted_info)

# Show remaining users (admins)
remaining_admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
remaining_admins = remaining_admins.distinct()
print('\nRemaining admin users:')
for a in remaining_admins:
    print(f' - ID: {a.id}, username: {a.username}, email: {a.email}, is_staff: {a.is_staff}, is_superuser: {a.is_superuser}')

print('\nDone.')

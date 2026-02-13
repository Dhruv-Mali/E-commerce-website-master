#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.loginsys.otp_models import UserPhone

User = get_user_model()

users = User.objects.all().order_by('id')
count = users.count()

print('\nUsers in database: {}\n'.format(count))
print('{:<5} {:<25} {:<30} {:<8} {:<10} {}'.format('ID','USERNAME','EMAIL','IS_STAFF','IS_ACTIVE','PHONE'))
print('-'*100)
for u in users:
    phone = None
    try:
        pp = UserPhone.objects.get(user=u)
        phone = pp.phone_number
    except UserPhone.DoesNotExist:
        phone = ''
    print('{:<5} {:<25} {:<30} {:<8} {:<10} {}'.format(u.id, u.username, (u.email or ''), str(u.is_staff), str(u.is_active), phone))

print('\n')

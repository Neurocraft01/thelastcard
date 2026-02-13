#!/usr/bin/env python
"""Quick script to check users in database."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from accounts.models import User

print("=" * 60)
print("USER DATABASE CHECK")
print("=" * 60)

total = User.objects.count()
users = User.objects.filter(role='USER').count()
admins = User.objects.filter(role='ADMIN').count()
superadmins = User.objects.filter(role='SUPER_ADMIN').count()

print(f"\nTotal users: {total}")
print(f"  - Regular users (USER): {users}")
print(f"  - Admins (ADMIN): {admins}")
print(f"  - Super admins (SUPER_ADMIN): {superadmins}")

print("\n" + "=" * 60)
print("ALL USERS IN DATABASE:")
print("=" * 60)

for user in User.objects.all():
    print(f"\nEmail: {user.email}")
    print(f"Role: {user.role}")
    print(f"Active: {user.is_active}")
    print(f"Cards: {user.cards.count()}")
    print("-" * 40)

if total == 0:
    print("\n⚠️  NO USERS FOUND IN DATABASE!")
    print("You need to create users first.")

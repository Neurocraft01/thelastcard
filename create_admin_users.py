#!/usr/bin/env python
"""
Create superadmin and admin users for Django project
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

def create_superadmin():
    """Create a superadmin user"""
    print("\n" + "="*60)
    print("CREATE SUPERADMIN (Full Access)")
    print("="*60)
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email is required!")
        return False
    
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    from getpass import getpass
    password = getpass("Password: ")
    password_confirm = getpass("Confirm Password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return False
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        return False
    
    try:
        user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"\n✅ Superadmin created successfully!")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.get_full_name()}")
        print(f"   Role: {user.get_role_display()}")
        print(f"   Superuser: {'Yes' if user.is_superuser else 'No'}")
        print(f"   Staff: {'Yes' if user.is_staff else 'No'}")
        return True
    except IntegrityError:
        print(f"❌ User with email '{email}' already exists!")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def create_admin():
    """Create a regular admin user (staff member)"""
    print("\n" + "="*60)
    print("CREATE ADMIN USER (Staff Access)")
    print("="*60)
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email is required!")
        return False
    
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    from getpass import getpass
    password = getpass("Password: ")
    password_confirm = getpass("Confirm Password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return False
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        return False
    
    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=False,
            role='admin'  # Set role to admin
        )
        print(f"\n✅ Admin user created successfully!")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.get_full_name()}")
        print(f"   Role: {user.get_role_display()}")
        print(f"   Superuser: {'Yes' if user.is_superuser else 'No'}")
        print(f"   Staff: {'Yes' if user.is_staff else 'No'}")
        return True
    except IntegrityError:
        print(f"❌ User with email '{email}' already exists!")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def list_admin_users():
    """List all existing admin and superadmin users"""
    print("\n" + "="*60)
    print("EXISTING ADMIN USERS")
    print("="*60)
    
    superadmins = User.objects.filter(is_superuser=True)
    admins = User.objects.filter(is_staff=True, is_superuser=False)
    
    if superadmins.exists():
        print("\n🔑 Superadmins:")
        for user in superadmins:
            print(f"   - {user.email} ({user.get_full_name()}) - Role: {user.get_role_display()}")
    else:
        print("\n⚠️  No superadmins found")
    
    if admins.exists():
        print("\n👤 Admin Users:")
        for user in admins:
            print(f"   - {user.email} ({user.get_full_name()}) - Role: {user.get_role_display()}")
    else:
        print("\n⚠️  No admin users found")
    
    print(f"\n📊 Total Users: {User.objects.count()}")
    print("="*60)


def main():
    print("\n" + "="*60)
    print("ADMIN USER MANAGEMENT")
    print("="*60)
    print("1. Create Superadmin (Full Access)")
    print("2. Create Admin User (Staff Access)")
    print("3. List Existing Admin Users")
    print("4. Exit")
    print("="*60)
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            create_superadmin()
        elif choice == '2':
            create_admin()
        elif choice == '3':
            list_admin_users()
        elif choice == '4':
            print("\n✅ Exiting...")
            break
        else:
            print("❌ Invalid choice! Please select 1-4")
        
        # Ask if they want to continue
        if choice in ['1', '2']:
            continue_choice = input("\nCreate another user? (y/n): ").strip().lower()
            if continue_choice != 'y':
                list_admin_users()
                break


if __name__ == '__main__':
    main()

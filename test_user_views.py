#!/usr/bin/env python
"""Test script to check user views."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from accounts.models import User
from accounts.views import SuperAdminUsersView, AdminUsersView

print("=" * 60)
print("TESTING USER VIEWS")
print("=" * 60)

# Get admin and superadmin users
try:
    admin_user = User.objects.filter(role='ADMIN').first()
    superadmin_user = User.objects.filter(role='SUPER_ADMIN').first()
    
    print(f"\nAdmin user: {admin_user.email if admin_user else 'NOT FOUND'}")
    print(f"Super admin user: {superadmin_user.email if superadmin_user else 'NOT FOUND'}")
    
    if not admin_user or not superadmin_user:
        print("\n⚠️  Missing admin or superadmin users!")
    else:
        # Test Super Admin Users View
        print("\n" + "=" * 60)
        print("TESTING SUPER ADMIN USERS VIEW")
        print("=" * 60)
        
        factory = RequestFactory()
        request = factory.get('/superadmin/users/')
        request.user = superadmin_user
        
        view = SuperAdminUsersView.as_view()
        response = view(request)
        
        print(f"Response status: {response.status_code}")
        print(f"Context data keys: {list(response.context_data.keys()) if hasattr(response, 'context_data') else 'No context'}")
        
        if hasattr(response, 'context_data') and 'users' in response.context_data:
            users = response.context_data['users']
            print(f"Number of users in context: {len(users)}")
            print("\nUsers:")
            for u in users:
                print(f"  - {u.email} ({u.role})")
        
        # Test Admin Users View
        print("\n" + "=" * 60)
        print("TESTING ADMIN USERS VIEW")
        print("=" * 60)
        
        request2 = factory.get('/admin-dashboard/users/')
        request2.user = admin_user
        
        view2 = AdminUsersView.as_view()
        response2 = view2(request2)
        
        print(f"Response status: {response2.status_code}")
        print(f"Context data keys: {list(response2.context_data.keys()) if hasattr(response2, 'context_data') else 'No context'}")
        
        if hasattr(response2, 'context_data') and 'users' in response2.context_data:
            users = response2.context_data['users']
            print(f"Number of users in context: {len(users)}")
            print("\nUsers:")
            for u in users:
                print(f"  - {u.email} ({u.role})")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

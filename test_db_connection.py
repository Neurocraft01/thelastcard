#!/usr/bin/env python
"""Test database connection for Django project"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nfc_platform.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

def test_database_connection():
    """Test database connection and basic queries"""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    try:
        # Display connection info
        db_engine = connection.settings_dict.get('ENGINE', 'Unknown')
        db_name = connection.settings_dict.get('NAME', 'Unknown')
        db_host = connection.settings_dict.get('HOST', 'localhost')
        db_port = connection.settings_dict.get('PORT', '')
        
        print(f"✓ Database Engine: {db_engine}")
        print(f"✓ Database Name: {db_name}")
        if db_host and db_host != 'localhost':
            print(f"✓ Database Host: {db_host}")
        if db_port:
            print(f"✓ Database Port: {db_port}")
        print()
        
        # Test 1: Basic connection and version
        with connection.cursor() as cursor:
            if 'postgresql' in db_engine:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                print(f"✓ PostgreSQL Version: {version.split(',')[0]}")
            else:
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                print(f"✓ SQLite Version: {version}")
        
        # Test 2: Query user count
        User = get_user_model()
        user_count = User.objects.count()
        print(f"✓ Users in database: {user_count}")
        
        # Test 3: Query cards
        from cards.models import NFCCard
        card_count = NFCCard.objects.count()
        print(f"✓ Cards in database: {card_count}")
        
        # Test 4: Query orders
        from orders.models import CardOrder
        order_count = CardOrder.objects.count()
        print(f"✓ Orders in database: {order_count}")
        
        # Test 5: Check database tables
        with connection.cursor() as cursor:
            if 'postgresql' in db_engine:
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✓ Total tables: {len(tables)}")
        
        print("=" * 60)
        print("✓ DATABASE CONNECTION: SUCCESS")
        print("✓ All queries executed successfully")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print("✗ DATABASE CONNECTION: FAILED")
        print(f"✗ Error: {str(e)}")
        print("=" * 60)
        return False
    
    return True

if __name__ == '__main__':
    test_database_connection()

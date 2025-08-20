#!/usr/bin/env python
"""
Database Migration Management Script for CauseHive Monolith

This script helps manage migrations across multiple databases.
Each service maintains its own database on Supabase.
"""
import os
import sys
import django
import time
from django.core.management import execute_from_command_line
from django.db import connections
from django.core.management.base import CommandError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'causehive_monolith.settings')
django.setup()

def check_database_connection(db_alias, max_retries=5, delay=2):
    """Check if database is accessible with retries"""
    for attempt in range(max_retries):
        try:
            conn = connections[db_alias]
            conn.ensure_connection()
            print(f"✅ Database {db_alias} connection successful")
            return True
        except Exception as e:
            print(f"⚠️  Database {db_alias} connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                print(f"❌ Database {db_alias} connection failed after {max_retries} attempts")
                return False
    return False

def migrate_database_safely(db_alias, app_labels=None):
    """Safely migrate a database with connection checks"""
    print(f"\n=== Migrating {db_alias} database ===")
    
    # Check connection first
    if not check_database_connection(db_alias):
        return False
    
    try:
        if app_labels:
            for app_label in app_labels:
                print(f"Migrating {app_label} to {db_alias}...")
                execute_from_command_line(['manage.py', 'migrate', app_label, '--database', db_alias])
        else:
            execute_from_command_line(['manage.py', 'migrate', '--database', db_alias])
        
        print(f"✅ Successfully migrated {db_alias}")
        return True
    except CommandError as e:
        if "No migrations to apply" in str(e):
            print(f"ℹ️  No migrations needed for {db_alias}")
            return True
        else:
            print(f"❌ Migration error for {db_alias}: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error migrating {db_alias}: {e}")
        return False

def migrate_all_databases():
    """Run migrations on all configured databases with proper app routing"""
    database_apps = {
        'default': ['users_n_auth', 'admin', 'auth', 'contenttypes', 'sessions', 'sites', 'allauth', 'account'],
        'cause_service': ['causes', 'categories'],
        'donation_service': ['donations', 'cart', 'payments', 'withdrawal_transfer'],
        'admin_service': ['admin_auth', 'dashboard', 'auditlog', 'notifications', 'management']
    }
    
    success_count = 0
    total_count = len(database_apps)
    
    for db_alias, app_labels in database_apps.items():
        if migrate_database_safely(db_alias, app_labels):
            success_count += 1
        else:
            print(f"⚠️  Continuing despite {db_alias} migration issues...")
    
    print(f"\n=== Migration Summary ===")
    print(f"Successfully migrated: {success_count}/{total_count} databases")
    
    if success_count == total_count:
        print("🎉 All databases migrated successfully!")
        return True
    else:
        print("⚠️  Some databases had migration issues")
        return success_count > 0  # Return True if at least one database migrated

def migrate_specific_app(app_label, database):
    """Migrate a specific app to its database"""
    print(f"\n=== Migrating {app_label} to {database} ===")
    return migrate_database_safely(database, [app_label])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'all':
            success = migrate_all_databases()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == 'app' and len(sys.argv) == 4:
            app_label = sys.argv[2]
            database = sys.argv[3]
            success = migrate_specific_app(app_label, database)
            sys.exit(0 if success else 1)
        else:
            print("Usage:")
            print("  python migrate_databases.py all")
            print("  python migrate_databases.py app <app_label> <database>")
            print("\nDatabases: default, cause_service, donation_service, admin_service")
    else:
        success = migrate_all_databases()
        sys.exit(0 if success else 1)

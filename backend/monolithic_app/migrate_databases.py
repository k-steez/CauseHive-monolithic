#!/usr/bin/env python
"""
Database Migration Management Script for CauseHive Monolith

This script helps manage migrations across multiple databases.
Each service maintains its own database on Supabase.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'causehive_monolith.settings')
django.setup()

from django.core.management.commands.migrate import Command as MigrateCommand

def migrate_all_databases():
    """Run migrations on all configured databases"""
    databases = ['default', 'causes_db', 'donations_db', 'admin_db']
    
    for db in databases:
        print(f"\n=== Migrating {db} database ===")
        try:
            execute_from_command_line(['manage.py', 'migrate', '--database', db])
            print(f"✅ Successfully migrated {db}")
        except Exception as e:
            print(f"❌ Error migrating {db}: {e}")

def migrate_specific_app(app_label, database):
    """Migrate a specific app to its database"""
    print(f"\n=== Migrating {app_label} to {database} ===")
    try:
        execute_from_command_line(['manage.py', 'migrate', app_label, '--database', database])
        print(f"✅ Successfully migrated {app_label} to {database}")
    except Exception as e:
        print(f"❌ Error migrating {app_label} to {database}: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'all':
            migrate_all_databases()
        elif sys.argv[1] == 'app' and len(sys.argv) == 4:
            app_label = sys.argv[2]
            database = sys.argv[3]
            migrate_specific_app(app_label, database)
        else:
            print("Usage:")
            print("  python migrate_databases.py all")
            print("  python migrate_databases.py app <app_label> <database>")
            print("\nDatabases: default, causes_db, donations_db, admin_db")
    else:
        migrate_all_databases()

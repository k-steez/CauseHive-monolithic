#!/bin/bash

# CauseHive Monolith Database Migration Script
# This script runs migrations for each database separately

echo "🚀 Starting database migrations for CauseHive Monolith..."

# Run migrations for default database (user service)
echo "📊 Migrating user service database (default)..."
python manage.py migrate --database=default

# Run migrations for causes database
echo "📊 Migrating cause service database (causes_db)..."
python manage.py migrate causes --database=causes_db
python manage.py migrate categories --database=causes_db

# Run migrations for donations database
echo "📊 Migrating donation processing service database (donations_db)..."
python manage.py migrate donations --database=donations_db
python manage.py migrate cart --database=donations_db
python manage.py migrate payments --database=donations_db
python manage.py migrate withdrawal_transfer --database=donations_db

# Run migrations for admin database
echo "📊 Migrating admin reporting service database (admin_db)..."
python manage.py migrate admin_auth --database=admin_db
python manage.py migrate dashboard --database=admin_db
python manage.py migrate auditlog --database=admin_db
python manage.py migrate notifications --database=admin_db
python manage.py migrate management --database=admin_db

echo "✅ All database migrations completed!"

# Create superuser prompt
echo "🔧 Would you like to create a superuser? (y/n)"
read -r create_superuser

if [[ $create_superuser =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo "🎉 CauseHive Monolith is ready!"

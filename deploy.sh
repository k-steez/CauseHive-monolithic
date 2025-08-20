#!/bin/bash

# Railway Deployment Script for CauseHive Monolith
# This script ensures Railway deploys from the monolithic app directory

echo "🚀 Starting Railway deployment for CauseHive Monolith..."

# Set the working directory to the monolithic app
cd backend/monolithic_app || {
    echo "❌ Error: backend/monolithic_app directory not found"
    exit 1
}

echo "📂 Current directory: $(pwd)"
echo "📋 Contents:"
ls -la

# Verify required files exist
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

if [ ! -f "railway.dockerfile" ]; then
    echo "❌ Error: railway.dockerfile not found"
    exit 1
fi

echo "✅ All required files found"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations for all databases
echo "🗄️ Running database migrations..."
python migrate_databases.py all

echo "✅ Railway deployment preparation complete!"
echo "🌐 Application ready to start with: gunicorn causehive_monolith.wsgi:application"

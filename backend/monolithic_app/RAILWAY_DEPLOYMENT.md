# CauseHive Monolithic Application - Railway Deployment Guide

## ✅ What's Been Created

Your CauseHive application has been successfully converted from a microservices architecture to a monolithic structure while maintaining database separation. Here's what's been set up:

### 📁 Project Structure
```
backend/monolithic_app/
├── manage.py                     # Django management script
├── requirements.txt              # All combined dependencies
├── migrate_databases.py          # Multi-database migration script
├── .env.template                 # Environment variables template
├── railway.dockerfile            # Railway-specific Docker config
├── railway.json                  # Railway deployment config
├── DEPLOYMENT.md                 # Detailed deployment guide
├── causehive_monolith/           # Main Django project
│   ├── settings.py               # Combined settings from all services
│   ├── urls.py                   # Unified URL routing
│   ├── db_router.py              # Multi-database routing
│   ├── wsgi.py                   # WSGI application
│   └── celery.py                 # Background tasks config
├── users_n_auth/                 # User service app
├── causes/                       # Cause management app  
├── categories/                   # Categories app
├── donations/                    # Donations app
├── cart/                         # Shopping cart app
├── payments/                     # Payment processing app
├── withdrawal_transfer/          # Withdrawals app
├── admin_auth/                   # Admin authentication app
├── dashboard/                    # Admin dashboard app
├── auditlog/                     # Audit logging app
├── notifications/                # Notifications app
├── management/                   # Admin management app
├── templates/                    # Django templates
├── static/                       # Static files
└── media/                        # Media files
```

### 🗄️ Database Architecture

The application maintains **4 separate Supabase databases**:

1. **User Service DB** (`default`)
   - Apps: `users_n_auth`
   - Purpose: User authentication, profiles, permissions

2. **Cause Service DB** (`causes_db`)
   - Apps: `causes`, `categories`
   - Purpose: Cause management and categorization

3. **Donation Service DB** (`donations_db`)
   - Apps: `donations`, `cart`, `payments`, `withdrawal_transfer`
   - Purpose: Payment processing and financial transactions

4. **Admin Service DB** (`admin_db`)
   - Apps: `admin_auth`, `dashboard`, `auditlog`, `notifications`, `management`
   - Purpose: Administrative functions and reporting

## 🚀 Railway Deployment Steps

### Step 1: Create Supabase Databases

Create 4 separate databases in Supabase:
- `causehive_users`
- `causehive_causes` 
- `causehive_donations`
- `causehive_admin`

### Step 2: Set Up Railway Project

1. **Connect GitHub Repository** to Railway
2. **Set Root Directory** to `/backend/monolithic_app` in Railway dashboard
3. **Choose Dockerfile** deployment (Railway will use `railway.dockerfile`)

### Step 3: Configure Environment Variables in Railway

Copy the environment variables from `.env.template` and set them in your Railway project:

**Essential Variables:**
```bash
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Database configurations for each service (copy 4 times with different prefixes)
USER_SERVICE_DB_NAME=causehive_users
USER_SERVICE_DB_USER=your_supabase_user
USER_SERVICE_DB_PASSWORD=your_supabase_password
USER_SERVICE_DB_HOST=your_supabase_host
USER_SERVICE_DB_PORT=5432

# Redis for background tasks
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/1

# Payment processing
PAYSTACK_PUBLIC_KEY=pk_live_xxx
PAYSTACK_SECRET_KEY=sk_live_xxx

ADMIN_SERVICE_API_KEY=your-admin-api-key
FRONTEND_URL=https://your-frontend-domain.com
```

### Step 4: Deploy

1. **Push to GitHub** - Railway will automatically deploy
2. **Monitor Logs** - Check Railway dashboard for deployment progress
3. **Verify Database Migrations** - All 4 databases will be migrated automatically

## 🔧 Key Features

### ✅ Unified API Endpoints
- All microservice endpoints are now under `/api/`
- Consistent authentication across all services
- Single deployment and management

### ✅ Database Isolation
- Each service domain maintains its own database
- Future microservice extraction remains possible
- Data integrity and separation preserved

### ✅ Background Tasks
- Celery configured for report generation
- Automated cause approval workflows
- Email notifications and processing

### ✅ Production Ready
- Gunicorn WSGI server
- Static file serving with WhiteNoise
- Security headers and HTTPS enforcement
- Structured logging for monitoring

## 📊 API Structure

After deployment, your API will be available at:

```bash
# User Management
POST /api/user/auth/signup/
POST /api/user/auth/login/
GET  /api/user/profile/

# Cause Management  
GET  /api/causes/
POST /api/causes/
GET  /api/causes/{id}/

# Donations & Payments
POST /api/donations/
GET  /api/donations/
POST /api/payments/initialize/

# Admin Dashboard
POST /api/admin/auth/login/
GET  /api/admin/dashboard/
GET  /api/admin/auditlog/
```

## 🎯 Next Steps

1. **Deploy to Railway** using the configuration provided
2. **Test all endpoints** to ensure proper functionality
3. **Configure your frontend** to use the new unified API
4. **Set up monitoring** and error tracking
5. **Configure backups** for your Supabase databases

## 🆘 Troubleshooting

- **Migration Issues**: Use `python migrate_databases.py all` to run all migrations
- **Import Errors**: Check that all required environment variables are set
- **Database Connection**: Verify Supabase credentials and network access
- **Static Files**: Ensure `python manage.py collectstatic` runs successfully

Your CauseHive application is now ready for Railway deployment! 🎉

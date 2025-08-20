# CauseHive Monolithic Application

This is the monolithic version of CauseHive, combining all microservices into a single Django application while maintaining separate Supabase databases for each service domain.

## Architecture Overview

The monolithic application combines four main services:
- **User Service**: User authentication, profiles, and management
- **Cause Service**: Cause creation, management, and categories
- **Donation Processing Service**: Donations, payments, cart, and withdrawals
- **Admin Reporting Service**: Admin authentication, dashboard, audit logs, and notifications

Each service maintains its own dedicated Supabase database for data isolation and scalability.

## Database Architecture

The application uses a custom database router to direct each app to its appropriate database:

- `default` (User Service DB): `users_n_auth`
- `causes_db` (Cause Service DB): `causes`, `categories`
- `donations_db` (Donation Service DB): `donations`, `cart`, `payments`, `withdrawal_transfer`
- `admin_db` (Admin Service DB): `admin_auth`, `dashboard`, `auditlog`, `notifications`, `management`

## Deployment on Railway

### Prerequisites

1. **Supabase Databases**: Create 4 separate Supabase databases
   - causehive_users
   - causehive_causes
   - causehive_donations
   - causehive_admin

2. **Redis Instance**: Set up Redis for Celery background tasks

3. **Paystack Account**: For payment processing

### Environment Variables

Set these environment variables in your Railway project:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Frontend URL
FRONTEND_URL=https://your-frontend-url.com

# User Service Database
USER_SERVICE_DB_NAME=causehive_users
USER_SERVICE_DB_USER=your_supabase_user
USER_SERVICE_DB_PASSWORD=your_supabase_password
USER_SERVICE_DB_HOST=your_supabase_host
USER_SERVICE_DB_PORT=5432

# Cause Service Database
CAUSE_SERVICE_DB_NAME=causehive_causes
CAUSE_SERVICE_DB_USER=your_supabase_user
CAUSE_SERVICE_DB_PASSWORD=your_supabase_password
CAUSE_SERVICE_DB_HOST=your_supabase_host
CAUSE_SERVICE_DB_PORT=5432

# Donation Service Database
DONATION_SERVICE_DB_NAME=causehive_donations
DONATION_SERVICE_DB_USER=your_supabase_user
DONATION_SERVICE_DB_PASSWORD=your_supabase_password
DONATION_SERVICE_DB_HOST=your_supabase_host
DONATION_SERVICE_DB_PORT=5432

# Admin Service Database
ADMIN_SERVICE_DB_NAME=causehive_admin
ADMIN_SERVICE_DB_USER=your_supabase_user
ADMIN_SERVICE_DB_PASSWORD=your_supabase_password
ADMIN_SERVICE_DB_HOST=your_supabase_host
ADMIN_SERVICE_DB_PORT=5432

# Redis Configuration
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/1

# Paystack Configuration
PAYSTACK_PUBLIC_KEY=pk_live_xxx
PAYSTACK_SECRET_KEY=sk_live_xxx

# Admin API Key
ADMIN_SERVICE_API_KEY=your-admin-api-key
```

### Railway Deployment Steps

1. **Connect Repository**: Connect your GitHub repository to Railway

2. **Set Root Directory**: Ensure Railway deploys from `/backend/monolithic_app`

3. **Configure Environment**: Add all the environment variables listed above

4. **Deploy**: Railway will automatically use the `railway.dockerfile` and run migrations

## API Endpoints

The monolithic application provides a unified API structure:

### User Service
- `POST /api/user/auth/signup/` - User registration
- `POST /api/user/auth/login/` - User login
- `GET /api/user/profile/` - User profile
- `PUT /api/user/profile/` - Update profile

### Cause Service
- `GET /api/causes/` - List causes
- `POST /api/causes/` - Create cause
- `GET /api/causes/{id}/` - Get cause details
- `PUT /api/causes/{id}/` - Update cause

### Donation Service
- `POST /api/donations/` - Create donation
- `GET /api/donations/` - List donations
- `POST /api/payments/initialize/` - Initialize payment
- `GET /api/cart/` - Get cart items

### Admin Service
- `POST /api/admin/auth/login/` - Admin login
- `GET /api/admin/dashboard/` - Dashboard data
- `GET /api/admin/auditlog/` - Audit logs
- `GET /api/admin/notifications/` - Notifications

## Database Management

### Running Migrations

The application includes a custom migration script:

```bash
# Migrate all databases
python migrate_databases.py all

# Migrate specific app to specific database
python migrate_databases.py app users_n_auth default
```

### Database Routing

The `DatabaseRouter` automatically routes:
- User models → `default` database
- Cause models → `causes_db` database  
- Donation models → `donations_db` database
- Admin models → `admin_db` database

## Background Tasks

Celery is configured for background tasks:
- Report generation (hourly)
- Pending cause polling (every 3 minutes)
- Email notifications
- Payment processing

## Security Features

- JWT Authentication across all services
- CORS configuration for frontend integration
- Rate limiting on API endpoints
- Secure password validation
- SSL/TLS enforcement in production

## Monitoring and Logging

- Structured logging for Railway
- Error tracking and reporting
- API request logging
- Database query monitoring

## Scaling Considerations

While monolithic, the application is designed for easy scaling:
- Separate databases allow for future service extraction
- Stateless design enables horizontal scaling
- Background task separation via Celery
- CDN-ready static file serving

## Support

For issues or questions:
1. Check the Railway deployment logs
2. Verify all environment variables are set
3. Ensure all Supabase databases are accessible
4. Check Redis connectivity for background tasks

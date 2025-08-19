# Railway Dockerfile for CauseHive Monolith
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=causehive_monolith.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/monolithic_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the monolithic app
COPY backend/monolithic_app/ .

# Create necessary directories
RUN mkdir -p staticfiles media

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import django; django.setup(); print('Django OK')" || exit 1

# Start command
CMD ["sh", "-c", "python migrate_databases.py all && gunicorn --bind 0.0.0.0:8000 --workers 3 causehive_monolith.wsgi:application"]

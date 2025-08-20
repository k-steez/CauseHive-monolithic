# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=causehive_monolith.settings
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/monolithic_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/monolithic_app/ .

# Create necessary directories
RUN mkdir -p staticfiles media logs

# Set default environment variables for build
ENV SECRET_KEY=build-time-secret-key-will-be-overridden
ENV DEBUG=False

# Collect static files during build
RUN python manage.py collectstatic --noinput --clear

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:$PORT/api/ready/ || exit 1

# Start command with proper error handling
CMD ["sh", "-c", "python migrate_databases.py all && exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 --access-logfile - --error-logfile - --log-level info causehive_monolith.wsgi:application"]

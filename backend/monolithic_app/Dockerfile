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
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media logs

# Create a non-root user first
RUN adduser --disabled-password --gecos '' appuser

# Collect static files (do this before changing user)
RUN python manage.py collectstatic --noinput --clear || echo "Static files collection failed, continuing..."

# Change ownership and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE $PORT

# Health check using the new endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:$PORT/api/ready/ || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting CauseHive Monolith..."\n\
echo "Running database migrations..."\n\
python migrate_databases.py all || echo "Migration issues detected, continuing..."\n\
echo "Starting Gunicorn server..."\n\
exec gunicorn --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    causehive_monolith.wsgi:application' > /app/start.sh

RUN chmod +x /app/start.sh

# Start command
CMD ["/app/start.sh"]

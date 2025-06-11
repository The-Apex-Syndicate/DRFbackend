# Start from official Python image
FROM python:3.11-slim as base

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=moveibackend.settings

# Set working directory
WORKDIR /moveibackend

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Collect static files
ENV DJANGO_SETTINGS_MODULE=moveibackend.settings.prod
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd --create-home appuser
USER appuser

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["DJANGO_SETTINGS_MODULE=moveibackend.settings.prod" ,"gunicorn", "moveibackend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=2"]
# Use official Python runtime as base image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies for GDAL and GeoDjango
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libproj-dev \
    libsqlite3-mod-spatialite \
    g++ \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Get GDAL version for Python package installation
RUN export GDAL_VERSION=$(gdal-config --version) && \
    echo "GDAL version: $GDAL_VERSION"

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir GDAL==$(gdal-config --version)

# Copy project files
COPY . /app/

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run migrations, create staff group, and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py create_staff_group && python manage.py runserver 0.0.0.0:8000"]


# Dockerfile for TradePulse - Unified Backend Deployment
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy wsgi entry point
COPY wsgi.py .

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Use Gunicorn with Uvicorn workers
CMD gunicorn wsgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 1
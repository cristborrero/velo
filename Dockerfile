FROM python:3.11-slim

# Install system dependencies (ffmpeg required for audio/video merging)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definition
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set default port environment variable
ENV PORT=10000
EXPOSE 10000

# Start server using Gunicorn WSGI binding to dynamic PORT
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 4 --worker-class gthread app:app"

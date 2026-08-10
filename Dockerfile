FROM python:3.11-slim

# Install ffmpeg and the Node.js runtime required by yt-dlp EJS challenges.
# yt-dlp currently requires Node.js 22+ for its Node JavaScript runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" \
        > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
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

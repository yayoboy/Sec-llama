# ============================================================================
# Sec-Llama LAN Server - Multi-stage Dockerfile
# ============================================================================

# Stage 1: Frontend Builder
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend files
COPY web_ui/frontend/package*.json ./
RUN npm ci --only=production

COPY web_ui/frontend/ ./
RUN npm run build


# Stage 2: Python Backend
FROM python:3.11-slim

LABEL maintainer="Sec-Llama Team"
LABEL description="Sec-Llama LAN Server - Security Testing Suite with Remote LLM"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    nmap \
    tcpdump \
    wireshark-common \
    tshark \
    build-essential \
    libpcap-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create app user (non-root)
RUN useradd -m -u 1000 -s /bin/bash secllama

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY core/ ./core/
COPY modules/ ./modules/
COPY web_ui/backend/ ./web_ui/backend/
COPY config/ ./config/
COPY database/ ./database/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy frontend build from previous stage
COPY --from=frontend-builder /frontend/dist ./web_ui/frontend/dist

# Create necessary directories
RUN mkdir -p /app/logs /app/reports /app/database /app/uploads /app/backups && \
    chown -R secllama:secllama /app

# Switch to non-root user
USER secllama

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application via entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

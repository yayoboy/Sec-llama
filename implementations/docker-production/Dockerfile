# Production Dockerfile for Web UI
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-mcp.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-mcp.txt

# Copy application code
COPY web/ ./web/
COPY cli/ ./cli/
COPY modules/ ./modules/
COPY config/ ./config/

# Create non-root user
RUN useradd -m -u 1000 secllama && \
    chown -R secllama:secllama /app

# Create directories
RUN mkdir -p /app/logs /app/reports /app/database && \
    chown -R secllama:secllama /app/logs /app/reports /app/database

USER secllama

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run server (production mode)
CMD ["python", "-m", "uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]

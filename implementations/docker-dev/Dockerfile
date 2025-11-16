# Main Dockerfile for Docker Dev - Web UI
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-mcp.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-mcp.txt

# Copy application code
COPY cli/ ./cli/
COPY mcp-server/ ./mcp-server/
COPY web/ ./web/
COPY modules/ ./modules/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create directories
RUN mkdir -p /app/logs /app/reports /app/database

# Expose ports
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command (can be overridden)
CMD ["python", "-m", "uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

# Multi-stage Dockerfile for Web UI Full

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY web_ui/frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY web_ui/frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Python Backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY web_ui/backend/ ./web_ui/backend/
COPY web/ ./web/
COPY modules/ ./modules/
COPY config/ ./config/

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/dist ./web_ui/frontend/dist

# Create directories
RUN mkdir -p /app/logs /app/reports /app/database /app/static

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run server
CMD ["python", "-m", "uvicorn", "web_ui.backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

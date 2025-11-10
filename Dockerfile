FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    tcpdump \
    wireless-tools \
    aircrack-ng \
    net-tools \
    iputils-ping \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p /app/reports /app/logs /app/database

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["sec-llama"]
CMD ["--help"]

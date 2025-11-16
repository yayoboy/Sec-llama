# 🐳 Sec-Llama Docker Stack - Complete Installation Guide

Complete guide for deploying Sec-Llama using Docker Stack with automated setup.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Detailed Installation](#detailed-installation)
5. [AI Configuration](#ai-configuration)
6. [Stack Management](#stack-management)
7. [Scaling & High Availability](#scaling--high-availability)
8. [Troubleshooting](#troubleshooting)
9. [Security](#security)

---

## 🎯 Overview

The Sec-Llama Docker Stack provides:

- ✅ **Fully automated installation** with single command
- ✅ **Complete environment setup** (PostgreSQL, Redis, Ollama, MCP Server, Web UI)
- ✅ **Web UI for AI configuration** - configure Ollama remotely, manage models, API keys
- ✅ **Automatic secrets management**
- ✅ **Health checks** for all services
- ✅ **Persistent volumes** for data
- ✅ **Nginx reverse proxy** (optional)
- ✅ **Automated backups** (optional)
- ✅ **Docker Swarm** for scaling

### Architecture

```
┌─────────────────────────────────────────────────┐
│                  Nginx (optional)               │
│            Reverse Proxy + SSL                  │
└────────────┬────────────────────────┬───────────┘
             │                        │
      ┌──────▼──────┐         ┌──────▼──────┐
      │   Web UI    │         │ MCP Server  │
      │   (Port     │         │   (Port     │
      │    8080)    │         │    8765)    │
      └──────┬──────┘         └──────┬──────┘
             │                       │
      ┌──────▼───────────────────────▼──────┐
      │            Ollama LLM                │
      │         (Port 11434)                 │
      └──────┬───────────────────────┬───────┘
             │                       │
      ┌──────▼──────┐         ┌──────▼──────┐
      │ PostgreSQL  │         │    Redis    │
      │  Database   │         │    Cache    │
      └─────────────┘         └─────────────┘
```

---

## 📥 Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+) or macOS
- **CPU**: 4+ cores recommended (for LLM inference)
- **RAM**: 8GB minimum, 16GB+ recommended
- **Disk**: 50GB+ free space (for models)
- **Docker**: 20.10.0+
- **Docker Compose**: 2.0.0+ (optional)

### Required Software

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker installation
docker --version
docker info

# Enable Docker Swarm (if not already enabled)
docker swarm init
```

---

## 🚀 Quick Start

### One-Command Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Run installation script
./scripts/install_stack.sh

# That's it! 🎉
```

### Access Points

After installation:

- **Web UI**: http://localhost:8080
- **MCP Server**: http://localhost:8765
- **Ollama API**: http://localhost:11434

Default credentials are saved in `.env` file.

---

## 📚 Detailed Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama
```

### Step 2: Run Installation Script

```bash
# Basic installation
./scripts/install_stack.sh

# With Nginx reverse proxy
./scripts/install_stack.sh --with-nginx

# With automatic backups
./scripts/install_stack.sh --with-backup

# Custom stack name
./scripts/install_stack.sh --stack-name my-sec-suite

# Full installation with all options
./scripts/install_stack.sh \
  --stack-name production-sec-llama \
  --with-nginx \
  --with-backup
```

### Step 3: Wait for Services

The installer will:

1. ✅ Check prerequisites
2. ✅ Initialize Docker Swarm
3. ✅ Generate secure passwords
4. ✅ Create .env configuration
5. ✅ Create Docker secrets
6. ✅ Build Docker images
7. ✅ Deploy stack
8. ✅ Pull default Ollama model

**Initial model download may take 5-15 minutes** depending on your connection.

### Step 4: Verify Installation

```bash
# Check stack services
docker stack services sec-llama

# View service logs
docker service logs -f sec-llama_web-ui

# Check service health
docker service ps sec-llama_web-ui
```

---

## 🤖 AI Configuration

### Via Web UI (Recommended)

1. **Open Web UI**: http://localhost:8080
2. **Navigate to AI Configuration**: Click "AI Configuration" in sidebar
3. **Configure Ollama**:
   - **Local Ollama**: `http://ollama:11434` (default in Docker)
   - **Remote Ollama**: `http://your-server-ip:11434`
   - **External Server**: `http://192.168.1.100:11434`

4. **Test Connection**: Click "Test Connection" button
5. **Manage Models**:
   - View installed models
   - Pull new models (e.g., `llama3.1:8b`, `mixtral:8x7b`)
   - Delete unused models
   - Test model generation

6. **Configure Default Model**:
   - Select default model for security analysis
   - Adjust temperature (0-2)
   - Set max tokens (128-8192)

### Remote Ollama Setup

To use Ollama running on a different machine:

#### On Remote Machine (Ollama Server)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Configure Ollama to accept external connections
export OLLAMA_HOST=0.0.0.0:11434

# Start Ollama
ollama serve
```

#### In Sec-Llama Web UI

1. Go to **AI Configuration**
2. Set Ollama Host: `http://REMOTE_IP:11434`
3. Click "Test Connection"
4. Save Configuration

### Multiple AI Providers

Configure multiple AI providers for failover:

```yaml
# In config/mcp_server_config.yaml
ai_providers:
  - provider_type: openai
    api_key: "sk-..."
    model: "gpt-4"
    enabled: false

  - provider_type: anthropic
    api_key: "sk-ant-..."
    model: "claude-3-opus"
    enabled: false

ai_fallback_enabled: true  # Use providers if Ollama fails
```

---

## 📊 Stack Management

### View Stack Status

```bash
# List all services
docker stack services sec-llama

# View detailed service info
docker service ls

# Check service logs
docker service logs sec-llama_web-ui
docker service logs sec-llama_mcp-server
docker service logs sec-llama_ollama

# Check service tasks (replicas)
docker service ps sec-llama_web-ui
```

### Update Stack

```bash
# Pull latest changes
git pull origin main

# Rebuild images
docker build -t sec-llama/web-ui:latest -f Dockerfile.web-ui .
docker build -t sec-llama/mcp-server:latest -f Dockerfile.mcp .

# Update stack (zero-downtime with replicas)
docker stack deploy -c docker-stack.yml sec-llama
```

### Remove Stack

```bash
# Remove entire stack
docker stack rm sec-llama

# Wait for cleanup (services stop)
watch docker stack ps sec-llama

# Optional: Remove volumes (CAUTION: Deletes all data!)
docker volume rm sec-llama_postgres-data
docker volume rm sec-llama_ollama-models
docker volume rm sec-llama_redis-data
```

### Backup Data

```bash
# Manual backup
docker exec $(docker ps -q -f name=sec-llama_postgres) \
  pg_dump -U sec_llama sec_llama | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore from backup
gunzip < backup_20240115.sql.gz | \
  docker exec -i $(docker ps -q -f name=sec-llama_postgres) \
  psql -U sec_llama sec_llama
```

---

## 📈 Scaling & High Availability

### Scale Services

```bash
# Scale Web UI to 3 replicas
docker service scale sec-llama_web-ui=3

# Scale MCP Server to 2 replicas
docker service scale sec-llama_mcp-server=2

# View scaled services
docker service ps sec-llama_web-ui
```

### Load Balancing

Docker Swarm automatically load balances across replicas.

For external load balancing with Nginx:

```bash
# Deploy with Nginx profile
./scripts/install_stack.sh --with-nginx

# Nginx will automatically load balance to all Web UI replicas
```

### High Availability Setup

For production HA:

```bash
# Multi-node Docker Swarm setup

# On manager node
docker swarm init --advertise-addr MANAGER_IP

# On worker nodes
docker swarm join --token TOKEN MANAGER_IP:2377

# Deploy stack across cluster
docker stack deploy -c docker-stack.yml sec-llama

# Services will be distributed across nodes
docker node ls
docker service ps sec-llama_web-ui
```

---

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check service status
docker service ps sec-llama_web-ui --no-trunc

# View logs
docker service logs --tail 100 sec-llama_web-ui

# Restart service
docker service update --force sec-llama_web-ui
```

### Ollama Model Download Stuck

```bash
# Check Ollama logs
docker service logs sec-llama_ollama

# Check Ollama status
curl http://localhost:11434/api/tags

# Manually pull model
docker exec $(docker ps -q -f name=sec-llama_ollama) \
  ollama pull llama3.1:8b
```

### Database Connection Errors

```bash
# Check PostgreSQL status
docker service logs sec-llama_postgres

# Test connection
docker exec -it $(docker ps -q -f name=sec-llama_postgres) \
  psql -U sec_llama -d sec_llama

# Reset database (CAUTION: Deletes all data!)
docker service update --force sec-llama_postgres
```

### Web UI Can't Connect to Ollama

1. **Check AI Status** in Web UI: http://localhost:8080/ai-config
2. **Test Connection** with correct host:
   - Inside Docker: `http://ollama:11434`
   - From host: `http://localhost:11434`
   - Remote: `http://REMOTE_IP:11434`

3. **Check Ollama logs**:
   ```bash
   docker service logs sec-llama_ollama
   ```

4. **Verify network**:
   ```bash
   docker network inspect sec-llama_sec-llama-internal
   ```

### Port Conflicts

```bash
# Change ports in .env file
nano .env

# Update these variables
WEB_UI_PORT=9080  # Instead of 8080
MCP_PORT=9765     # Instead of 8765
OLLAMA_PORT=11435 # Instead of 11434

# Redeploy stack
docker stack deploy -c docker-stack.yml sec-llama
```

---

## 🔒 Security

### Change Default Passwords

```bash
# Edit .env file
nano .env

# Change passwords
POSTGRES_PASSWORD=your-strong-password
REDIS_PASSWORD=your-strong-password
SECRET_KEY=your-secret-key

# Recreate secrets
docker secret rm postgres_password redis_password secret_key
echo "your-strong-password" | docker secret create postgres_password -
echo "your-strong-password" | docker secret create redis_password -
echo "your-secret-key" | docker secret create secret_key -

# Redeploy
docker stack deploy -c docker-stack.yml sec-llama
```

### Enable HTTPS with Nginx

```bash
# Generate self-signed certificate (development)
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Or use Let's Encrypt (production)
certbot certonly --standalone -d your-domain.com

# Deploy with Nginx
./scripts/install_stack.sh --with-nginx
```

### Restrict Network Access

```bash
# Edit .env file
nano .env

# Restrict to specific networks
ALLOWED_NETWORKS=192.168.1.0/24,10.0.0.0/8

# Redeploy
docker stack deploy -c docker-stack.yml sec-llama
```

### API Key Authentication

1. **Create API Key** in Web UI: http://localhost:8080/api-keys
2. **Copy generated key** (shown only once!)
3. **Use in API calls**:
   ```bash
   curl -H "X-API-Key: your-api-key" \
     http://localhost:8765/api/tools
   ```

---

## 📱 Common Commands

```bash
# View all services
docker stack services sec-llama

# Scale service
docker service scale sec-llama_web-ui=3

# View logs
docker service logs -f sec-llama_web-ui

# Update service
docker service update --force sec-llama_web-ui

# Restart service
docker service update --force sec-llama_web-ui

# Remove stack
docker stack rm sec-llama

# View volumes
docker volume ls

# Backup database
./scripts/backup.sh

# Check Ollama models
curl http://localhost:11434/api/tags

# Pull Ollama model
docker exec $(docker ps -q -f name=sec-llama_ollama) \
  ollama pull codellama:13b
```

---

## 🆘 Getting Help

- **Documentation**: [docs/](../docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)

---

## 📝 Next Steps

After successful installation:

1. ✅ **Configure AI** in Web UI: http://localhost:8080/ai-config
2. ✅ **Create API Keys**: http://localhost:8080/api-keys
3. ✅ **Explore Tools**: http://localhost:8080/tools
4. ✅ **Run Security Scans**: Try network discovery and vulnerability scanning
5. ✅ **Check Audit Logs**: http://localhost:8080/audit-logs

---

**Made with ❤️ by the Sec-Llama Team**

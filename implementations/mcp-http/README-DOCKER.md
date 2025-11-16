# MCP HTTP - Docker Deployment

Quick guide for deploying MCP HTTP Server with Docker.

## 🚀 Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and set secure API keys
nano .env

# 3. Start services
docker-compose up -d

# 4. Pull Ollama model
docker-compose exec ollama ollama pull llama3.1:8b

# 5. Check health
curl http://localhost:8765/health
```

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- (Optional) NVIDIA GPU + nvidia-docker for GPU acceleration

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```bash
# Generate secure API key
MCP_API_KEYS=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Set in .env
MCP_API_KEYS=your-generated-key-here
MCP_PORT=8765
OLLAMA_PORT=11434
LOG_LEVEL=INFO
```

### GPU Support

If you have NVIDIA GPU:

```yaml
# Already configured in docker-compose.yml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

## 📊 Services

| Service | Port | Description |
|---------|------|-------------|
| mcp-server | 8765 | MCP HTTP/SSE server |
| ollama | 11434 | LLM inference server |

## 🎯 Usage

### Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f mcp-server
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes data!)
docker-compose down -v
```

### Manage Ollama Models

```bash
# Pull model
docker-compose exec ollama ollama pull llama3.1:8b

# List models
docker-compose exec ollama ollama list

# Remove model
docker-compose exec ollama ollama rm llama3.1:8b
```

### Test MCP Server

```bash
# Health check
curl http://localhost:8765/health

# List tools (requires API key)
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8765/sse

# Call tool
curl -X POST http://localhost:8765/tools/network_scan \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subnet": "192.168.1.0/24"}'
```

## 🔒 Security

### API Keys

**IMPORTANT:** Change the default API key in production!

```bash
# Generate secure key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Update .env
MCP_API_KEYS=your-new-secure-key
```

### Network Security

```bash
# Expose only on localhost
# Edit docker-compose.yml:
ports:
  - "127.0.0.1:8765:8765"  # Only localhost

# Or use nginx reverse proxy with SSL
```

### Firewall

```bash
# Allow only from specific IP
sudo ufw allow from 192.168.1.0/24 to any port 8765

# Or specific IP
sudo ufw allow from 192.168.1.100 to any port 8765
```

## 📈 Monitoring

### Logs

```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail 100

# Specific service
docker-compose logs -f mcp-server
```

### Resource Usage

```bash
# Container stats
docker-compose stats

# Specific container
docker stats sec-llama-mcp-http
```

### Health Checks

```bash
# Check all services
docker-compose ps

# Check specific service
curl http://localhost:8765/health
curl http://localhost:11434/api/tags
```

## 🔄 Updates

```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose build mcp-server
docker-compose up -d mcp-server
```

## 🐛 Troubleshooting

### MCP Server not starting

```bash
# Check logs
docker-compose logs mcp-server

# Check if port is already in use
lsof -i :8765

# Restart service
docker-compose restart mcp-server
```

### Ollama connection errors

```bash
# Check Ollama is running
docker-compose ps ollama

# Check Ollama health
curl http://localhost:11434/api/tags

# Restart Ollama
docker-compose restart ollama
```

### GPU not detected

```bash
# Check nvidia-docker
nvidia-smi

# Check docker can access GPU
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# If not working, install nvidia-container-toolkit
```

### Permission errors

```bash
# Fix ownership
sudo chown -R $USER:$USER logs/ reports/ database/

# Or run as root (not recommended)
sudo docker-compose up -d
```

## 📚 Advanced

### Custom Configuration

Create `config/config.yaml`:

```yaml
ollama:
  host: http://ollama:11434
  model: llama3.1:8b
  timeout: 120

server:
  port: 8765
  allowed_origins:
    - "*"
  rate_limit:
    enabled: true
    requests_per_minute: 60
```

Mount in docker-compose.yml:

```yaml
volumes:
  - ./config/config.yaml:/app/config/config.yaml:ro
```

### Multi-instance Deployment

```bash
# Scale MCP servers
docker-compose up -d --scale mcp-server=3

# Use nginx for load balancing
```

### Backup & Restore

```bash
# Backup volumes
docker run --rm \
  -v sec-llama-mcp-network_ollama_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/ollama-backup.tar.gz -C /data .

# Restore
docker run --rm \
  -v sec-llama-mcp-network_ollama_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/ollama-backup.tar.gz -C /data
```

## 🔗 Links

- [Main README](README.md)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Ollama Docs](https://ollama.com/docs)

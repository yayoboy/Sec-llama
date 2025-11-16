# Web UI Full - Docker Deployment

Quick guide for deploying Web UI with Docker.

## 🚀 Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Generate secure secrets
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env
python3 -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_hex(16))" >> .env

# 3. Edit .env if needed
nano .env

# 4. Start all services
docker-compose up -d

# 5. Pull Ollama model
docker-compose exec ollama ollama pull llama3.1:8b

# 6. Open browser
open http://localhost:8080
```

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ RAM (16GB recommended for LLM)
- (Optional) NVIDIA GPU for faster inference

## 🔧 Services

| Service | Port | Description |
|---------|------|-------------|
| web-ui | 8080 | Web interface |
| postgres | 5432 | Database |
| redis | 6379 | Cache |
| ollama | 11434 | LLM server |

## 📊 Usage

### Start Services

```bash
docker-compose up -d
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web-ui
```

### Stop Services

```bash
docker-compose down

# Remove volumes (CAUTION!)
docker-compose down -v
```

## 🎯 Configuration

### AI Configuration via UI

1. Open http://localhost:8080
2. Navigate to **AI Configuration**
3. Configure Ollama host (default: `http://ollama:11434`)
4. Pull models
5. Test generation

### Environment Variables

Key variables in `.env`:

```bash
# Application
WEB_UI_PORT=8080
SECRET_KEY=your-secure-key

# Database
POSTGRES_PASSWORD=your-secure-password

# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3.1:8b
```

## 🔒 Security

### Production Deployment

```bash
# 1. Set strong passwords
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_hex(16))")
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# 2. Disable debug
DEBUG=false

# 3. Use nginx reverse proxy with SSL
# 4. Set allowed origins
```

### Backup Database

```bash
# Backup
docker-compose exec postgres pg_dump -U sec_llama sec_llama > backup.sql

# Restore
docker-compose exec -T postgres psql -U sec_llama sec_llama < backup.sql
```

## 📈 Monitoring

```bash
# Container stats
docker-compose stats

# Health checks
curl http://localhost:8080/health
curl http://localhost:11434/api/tags
```

## 🔄 Updates

```bash
# Pull latest
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Frontend not loading

```bash
# Rebuild frontend
docker-compose build web-ui
docker-compose up -d web-ui
```

### Database connection errors

```bash
# Check postgres
docker-compose ps postgres
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### Ollama errors

```bash
# Check logs
docker-compose logs ollama

# Pull model manually
docker-compose exec ollama ollama pull llama3.1:8b
```

## 📚 Advanced

### Custom Models

```bash
# Pull larger model
docker-compose exec ollama ollama pull llama3.1:70b

# Configure in UI or .env
OLLAMA_MODEL=llama3.1:70b
```

### Scale Services

```bash
# Not applicable for docker-compose
# Use docker-dev or docker-production for scaling
```

### External Ollama

```yaml
# Edit docker-compose.yml or .env
OLLAMA_HOST=http://192.168.1.100:11434

# Comment out ollama service
# Update web-ui depends_on
```

## 🔗 Links

- [Main README](README.md)
- [MCP HTTP Docker](../mcp-http/README-DOCKER.md)
- [Docker Production](../docker-production/README.md)

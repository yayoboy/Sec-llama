# Docker Dev - Development Environment

Ambiente di sviluppo completo con Docker Compose per development.

## 🚀 Quick Start

```bash
# Avvia tutti i servizi
docker-compose up -d

# Vedi logs
docker-compose logs -f

# Accedi: http://localhost:8080
```

## 📦 Cosa Include

### Services

- **PostgreSQL** - Database (porta 5432)
- **Redis** - Cache e sessions (porta 6379)
- **Ollama** - LLM locale (porta 11434)
- **MCP Server** - MCP HTTP/SSE (porta 8765)
- **Web UI** - Interfaccia web (porta 8080)

### Features

- ✅ **Hot Reload** - Auto-reload su modifiche codice
- ✅ **Volume Mounting** - Codice montato per sviluppo
- ✅ **Debug Support** - Porte esposte per debugging
- ✅ **Database GUI** - pgAdmin disponibile
- ✅ **Log Aggregation** - Tutti i log centralizzati

## 🔧 Configurazione

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: sec_llama
      POSTGRES_USER: sec_llama
      POSTGRES_PASSWORD: dev_password_change_me
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  mcp-server:
    build:
      context: ../../
      dockerfile: implementations/mcp-http/Dockerfile
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - DATABASE_URL=postgresql://sec_llama:dev_password_change_me@postgres/sec_llama
      - REDIS_URL=redis://redis:6379
    ports:
      - "8765:8765"
    volumes:
      - ../../shared:/app/shared:ro
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
      - ollama
    restart: unless-stopped

  web-ui:
    build:
      context: ../../
      dockerfile: implementations/web-ui-full/Dockerfile.dev
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - DATABASE_URL=postgresql://sec_llama:dev_password_change_me@postgres/sec_llama
      - REDIS_URL=redis://redis:6379
      - MCP_SERVER_URL=http://mcp-server:8765
    ports:
      - "8080:8080"
      - "3000:3000"  # Frontend dev server
    volumes:
      - ../../shared:/app/shared:ro
      - ../../implementations/web-ui-full/backend:/app/backend
      - ../../implementations/web-ui-full/frontend:/app/frontend
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
      - ollama
      - mcp-server
    command: npm run dev
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

### Environment Variables

Crea `.env`:

```bash
# Database
POSTGRES_DB=sec_llama
POSTGRES_USER=sec_llama
POSTGRES_PASSWORD=dev_password_change_me

# Redis
REDIS_PASSWORD=

# Ollama
OLLAMA_HOST=http://ollama:11434
DEFAULT_MODEL=llama3.1:8b

# MCP
MCP_API_KEYS=dev-api-key-change-me

# Web UI
SECRET_KEY=dev-secret-key-change-me
DEBUG=true
```

## 🎨 Utilizzo

### Start/Stop

```bash
# Avvia tutti i servizi
docker-compose up -d

# Avvia in foreground (vedi logs)
docker-compose up

# Stop
docker-compose down

# Stop e rimuovi volumi (ATTENZIONE: cancella dati!)
docker-compose down -v

# Restart singolo servizio
docker-compose restart web-ui
```

### Logs

```bash
# Tutti i logs
docker-compose logs -f

# Logs singolo servizio
docker-compose logs -f web-ui
docker-compose logs -f mcp-server
docker-compose logs -f ollama

# Ultimi 100 righe
docker-compose logs --tail 100 -f
```

### Shell Access

```bash
# Bash in web-ui
docker-compose exec web-ui bash

# Bash in mcp-server
docker-compose exec mcp-server bash

# PostgreSQL CLI
docker-compose exec postgres psql -U sec_llama -d sec_llama

# Redis CLI
docker-compose exec redis redis-cli
```

### Database Management

```bash
# Backup database
docker-compose exec postgres pg_dump -U sec_llama sec_llama > backup.sql

# Restore database
docker-compose exec -T postgres psql -U sec_llama sec_llama < backup.sql

# Reset database
docker-compose down
docker volume rm docker-dev_postgres_data
docker-compose up -d
```

### Pull Ollama Model

```bash
# Pull default model
docker-compose exec ollama ollama pull llama3.1:8b

# Pull larger model
docker-compose exec ollama ollama pull llama3.1:70b

# List models
docker-compose exec ollama ollama list
```

## 🔧 Development Workflow

### Backend Development

1. Modifica file in `implementations/web-ui-full/backend/`
2. Il server si riavvia automaticamente (hot reload)
3. Test: `http://localhost:8080/docs`

### Frontend Development

1. Modifica file in `implementations/web-ui-full/frontend/src/`
2. Vite si ricarica automaticamente
3. Frontend dev server: `http://localhost:3000`
4. API proxy verso backend: `http://localhost:8080`

### Shared Libraries

1. Modifica file in `shared/`
2. Restart servizi che usano le librerie:
   ```bash
   docker-compose restart web-ui mcp-server
   ```

### Database Migrations

```bash
# Create migration
docker-compose exec web-ui alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec web-ui alembic upgrade head

# Rollback
docker-compose exec web-ui alembic downgrade -1
```

## 🐛 Debugging

### VSCode Remote Debugging

Aggiungi a `docker-compose.yml` nel servizio web-ui:

```yaml
environment:
  - DEBUGPY=true
ports:
  - "5678:5678"  # Debug port
```

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Remote Attach",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "/app"
        }
      ]
    }
  ]
}
```

### PyCharm Remote Debugging

1. Run → Edit Configurations
2. Add Python Remote Debug
3. Host: localhost, Port: 5678
4. Start debug session

## 📊 Monitoring

### Health Checks

```bash
# Web UI
curl http://localhost:8080/health

# MCP Server
curl http://localhost:8765/health

# Ollama
curl http://localhost:11434/api/tags

# PostgreSQL
docker-compose exec postgres pg_isready -U sec_llama

# Redis
docker-compose exec redis redis-cli ping
```

### Resource Usage

```bash
# Container stats
docker-compose stats

# Disk usage
docker-compose exec web-ui df -h

# Memory usage
docker-compose exec web-ui free -h
```

## 🆘 Troubleshooting

### Porte già in uso

```bash
# Trova processo usando la porta
lsof -i :8080
lsof -i :5432

# Uccidi processo
kill -9 PID

# O cambia porta in docker-compose.yml
```

### Container non parte

```bash
# Vedi logs dettagliati
docker-compose logs web-ui

# Rebuild immagine
docker-compose build --no-cache web-ui
docker-compose up -d web-ui
```

### Database connection errors

```bash
# Verifica database running
docker-compose ps postgres

# Check connessione
docker-compose exec postgres psql -U sec_llama -c "SELECT 1"

# Reset database
docker-compose down
docker volume rm docker-dev_postgres_data
docker-compose up -d
```

### Ollama out of memory

```bash
# Check GPU
nvidia-smi

# Usa modello più piccolo
docker-compose exec ollama ollama pull llama3.1:8b

# Aumenta memoria
# Modifica docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 16G
```

### Hot reload non funziona

```bash
# Verifica volumi montati
docker-compose exec web-ui ls -la /app/backend

# Restart container
docker-compose restart web-ui

# Rebuild
docker-compose up -d --build web-ui
```

## 🧪 Testing

### Run Tests

```bash
# Backend tests
docker-compose exec web-ui pytest

# Frontend tests
docker-compose exec web-ui npm test

# Integration tests
docker-compose exec web-ui pytest tests/integration/

# Coverage
docker-compose exec web-ui pytest --cov=backend --cov-report=html
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py --host http://localhost:8080
```

## 🚀 Performance Tips

1. **Use volumes for code** - Già configurato
2. **Limit log size** - Aggiungi a docker-compose.yml:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```
3. **Dedicated network** - Usa network dedicata
4. **Resource limits** - Setta limiti CPU/RAM
5. **Cache dependencies** - Usa buildkit con cache

## 📚 Links

- **[Docker Compose Docs](https://docs.docker.com/compose/)** - Official documentation
- **[Web UI Guide](../web-ui-full/README.md)** - Web UI documentation
- **[MCP HTTP Guide](../mcp-http/README.md)** - MCP server documentation

---

**Note:** Questo è un ambiente di SVILUPPO. Per produzione usa [Docker Production](../docker-production/README.md).

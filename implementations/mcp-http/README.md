# MCP HTTP - Remote MCP Server

Server MCP con transport HTTP/SSE per deployment LAN e accesso remoto.

## 🚀 Quick Start

```bash
# Setup (una volta)
./setup.sh

# Genera API key
export MCP_API_KEYS=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Avvia server
MCP_API_KEYS="$MCP_API_KEYS" ./start.sh

# Accedi da: http://localhost:8765
```

## 📦 Installazione

```bash
./setup.sh
```

Questo configura:
- Virtual environment Python
- Dipendenze MCP e FastAPI
- Collegamenti ai moduli shared
- Configurazione server HTTP

## 🎯 Features

### HTTP/SSE Transport
- ✅ **Remote Access** - Accesso da qualsiasi client sulla rete
- ✅ **Multi-Client** - Supporto clienti multipli simultanei
- ✅ **API Key Auth** - Autenticazione sicura
- ✅ **Rate Limiting** - Protezione contro abusi
- ✅ **Audit Logging** - Log completo di tutte le operazioni
- ✅ **CORS Support** - Configurabile per client web

### Security Tools via HTTP
Tutti gli 8+ strumenti di sicurezza disponibili via HTTP:
- Network scanning
- Port scanning
- Code analysis
- CVE lookup
- IOC analysis
- Container scanning
- Exploit search
- Payload generation

## 🔧 Configurazione

### API Keys

#### Generazione Automatica
```bash
./start.sh --generate-key
```

#### Generazione Manuale
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### Uso
```bash
# Singola chiave
export MCP_API_KEYS="your-api-key-here"

# Multiple chiavi (comma-separated)
export MCP_API_KEYS="key1,key2,key3"

# Da file
export MCP_API_KEYS=$(cat api_keys.txt)
```

### Configurazione Server

Modifica `config.yaml`:

```yaml
server:
  host: 0.0.0.0  # Listen su tutte le interfacce
  port: 8765
  allowed_origins:
    - "*"  # Permetti tutti (dev only)
    # - "https://yourdomain.com"  # Produzione
  rate_limit:
    enabled: true
    requests_per_minute: 60

ollama:
  host: http://localhost:11434
  model: llama3.1:8b
  timeout: 120
  enabled: true

security:
  require_api_key: true
  audit_log: true
  allowed_networks:
    - "0.0.0.0/0"  # Permetti tutti (dev only)
    # - "192.168.1.0/24"  # Solo LAN locale
```

### Porte Personalizzate

```bash
# Modifica .env o esporta variabile
export MCP_PORT=9000
./start.sh
```

## 🎨 Utilizzo

### Da Client MCP

Qualsiasi client MCP può connettersi:

```typescript
// JavaScript/TypeScript client
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const transport = new SSEClientTransport(
  new URL("http://your-server:8765/sse"),
  {
    headers: {
      "Authorization": "Bearer your-api-key"
    }
  }
);

const client = new Client({ name: "security-client", version: "1.0.0" }, {});
await client.connect(transport);

// List available tools
const tools = await client.listTools();

// Call a tool
const result = await client.callTool({
  name: "network_scan",
  arguments: {
    subnet: "192.168.1.0/24"
  }
});
```

### Da curl (Testing)

```bash
# Health check
curl http://localhost:8765/health

# List tools (requires API key)
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8765/sse

# Call tool via HTTP POST
curl -X POST http://localhost:8765/tools/network_scan \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subnet": "192.168.1.0/24"}'
```

### Da Claude Desktop

Configura `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sec-llama-remote": {
      "url": "http://your-server:8765/sse",
      "headers": {
        "Authorization": "Bearer your-api-key"
      }
    }
  }
}
```

## 🐳 Docker Deployment

### Quick Start

```bash
docker build -t sec-llama/mcp-http .
docker run -d \
  --name sec-llama-mcp \
  -p 8765:8765 \
  -e MCP_API_KEYS="your-api-key" \
  sec-llama/mcp-http
```

### Docker Compose

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "8765:8765"
    environment:
      - MCP_API_KEYS=${MCP_API_KEYS}
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

Start:
```bash
export MCP_API_KEYS=$(python3 -c "import secrets; print(secrets.token_hex(32))")
docker-compose up -d

# Pull model
docker-compose exec ollama ollama pull llama3.1:8b
```

## 🔒 Sicurezza

### HTTPS con Nginx

Configura Nginx come reverse proxy:

```nginx
server {
    listen 443 ssl http2;
    server_name mcp.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE support
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=mcp_limit:10m rate=10r/s;
    limit_req zone=mcp_limit burst=20 nodelay;
}
```

### Firewall

```bash
# Solo LAN locale
sudo ufw allow from 192.168.1.0/24 to any port 8765

# Specifica IP
sudo ufw allow from 192.168.1.100 to any port 8765
```

### Best Practices

1. **Usa HTTPS** in produzione (Nginx + Let's Encrypt)
2. **Genera API keys forti** (32+ caratteri)
3. **Limita allowed_networks** alla tua LAN
4. **Abilita audit logging** per tracking
5. **Rate limiting** per prevenire abusi
6. **Rotazione API keys** periodica
7. **Backup logs** regolari

## 📊 Monitoring & Logs

### Logs

```bash
# Application logs
tail -f logs/mcp_http.log

# Access logs
tail -f logs/access.log

# Audit logs
tail -f logs/audit.log
```

### Health Check

```bash
# Basic health
curl http://localhost:8765/health

# Detailed status
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8765/status
```

### Metrics

Il server espone metriche:
- Request count per tool
- Response times
- Error rates
- Active connections
- API key usage

Accedi via:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8765/metrics
```

## 🆘 Troubleshooting

### Server non parte

```bash
# Check porte in uso
lsof -i :8765

# Check logs
tail -f logs/mcp_http.log

# Test configurazione
python -m mcp_server.http_transport --test-config
```

### Errori di autenticazione

```bash
# Verifica API key
echo $MCP_API_KEYS

# Test con curl
curl -v -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8765/health
```

### Ollama non raggiungibile

```bash
# Test Ollama
curl http://localhost:11434/api/tags

# Se Ollama è remoto
curl http://OLLAMA_IP:11434/api/tags

# Verifica config
cat config.yaml | grep -A 5 ollama
```

### Problemi CORS

Se ricevi errori CORS da client web:

1. Modifica `config.yaml`:
```yaml
server:
  allowed_origins:
    - "https://your-frontend-domain.com"
```

2. Restart server

## 🔄 Aggiornamento

```bash
git pull origin main
./setup.sh
# Riavvia server
```

## 📚 API Reference

### Endpoints

| Endpoint | Method | Auth | Descrizione |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/sse` | GET | Yes | SSE endpoint (MCP) |
| `/tools` | GET | Yes | List tools |
| `/tools/{name}` | POST | Yes | Call tool |
| `/status` | GET | Yes | Server status |
| `/metrics` | GET | Yes | Server metrics |

### Authentication

Usa header `Authorization`:
```
Authorization: Bearer your-api-key-here
```

### Rate Limits

Default: 60 requests/minute per IP

Headers di risposta:
- `X-RateLimit-Limit`: Limite totale
- `X-RateLimit-Remaining`: Richieste rimanenti
- `X-RateLimit-Reset`: Timestamp reset

## 🔗 Links

- **[MCP Protocol](https://modelcontextprotocol.io)** - Model Context Protocol docs
- **[MCP SDK](https://github.com/modelcontextprotocol/sdk)** - Official SDK
- **[Sec-Llama Main](../../README.md)** - Main documentation

---

**Note:** Per uso locale con Claude Desktop, considera [MCP stdio](../mcp-stdio/README.md) che è più semplice da configurare.

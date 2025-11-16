# 📘 Guida Deployment Completa - Sec-Llama

Documentazione completa per il deployment di Sec-Llama su server LAN con Docker e LLM remoto.

---

## 📋 Indice

1. [Panoramica Sistema](#panoramica-sistema)
2. [Architettura](#architettura)
3. [Requisiti](#requisiti)
4. [Setup Rapido](#setup-rapido)
5. [Configurazione Dettagliata](#configurazione-dettagliata)
6. [Deployment Methods](#deployment-methods)
7. [Verifica e Testing](#verifica-e-testing)
8. [Manutenzione](#manutenzione)
9. [Troubleshooting](#troubleshooting)
10. [Security Best Practices](#security-best-practices)

---

## 🎯 Panoramica Sistema

### Cosa è Sec-Llama?

Sec-Llama è una **piattaforma completa di cybersecurity testing** che combina:

- **Security Testing Tools**: Network scanning, SAST, vulnerability assessment
- **AI-Powered Analysis**: Analisi intelligente tramite LLM locale
- **Web UI Moderna**: Interfaccia completa per gestione e configurazione
- **LAN Deployment**: Ottimizzato per deployment su rete locale privata
- **Production Ready**: PostgreSQL, Redis, health checks, migrations

### Perché Sec-Llama?

✅ **100% Privato**: Tutti i dati rimangono sulla tua rete LAN
✅ **LLM Locale**: Usa il tuo hardware per l'AI (Ollama/LM Studio)
✅ **Modulare**: Ogni tool security è indipendente
✅ **Scalabile**: Da setup development a production cluster
✅ **Open Source**: Codice completamente aperto e modificabile

---

## 🏗️ Architettura

### Architettura Completa

```
┌───────────────────────────────────────────────────────────────┐
│                     LAN Network (192.168.1.0/24)              │
│                                                               │
│  ┌─────────────────┐              ┌──────────────────────┐   │
│  │ PC LLM          │              │ Server Sec-Llama     │   │
│  │ 192.168.1.100   │              │ 192.168.1.10         │   │
│  │                 │              │                      │   │
│  │  ┌───────────┐  │              │  ┌────────────────┐ │   │
│  │  │  Ollama   │  │◄────────────▶│  │  Web UI        │ │   │
│  │  │  :11434   │  │   HTTP API   │  │  :8080         │ │   │
│  │  │           │  │              │  │                │ │   │
│  │  │ Models:   │  │              │  │  FastAPI       │ │   │
│  │  │ - llama3.1│  │              │  │  + Vue.js      │ │   │
│  │  │ - mistral │  │              │  └────────┬───────┘ │   │
│  │  └───────────┘  │              │           │         │   │
│  │                 │              │  ┌────────▼───────┐ │   │
│  │   OR            │              │  │  PostgreSQL    │ │   │
│  │                 │              │  │  :5432         │ │   │
│  │  ┌───────────┐  │              │  │                │ │   │
│  │  │ LM Studio │  │              │  │  - Users       │ │   │
│  │  │  :1234    │  │              │  │  - Scans       │ │   │
│  │  └───────────┘  │              │  │  - Reports     │ │   │
│  └─────────────────┘              │  └────────────────┘ │   │
│                                   │                      │   │
│                                   │  ┌────────────────┐ │   │
│  ┌─────────────────┐              │  │  Redis         │ │   │
│  │ Client Browser  │              │  │  :6379         │ │   │
│  │                 │              │  │                │ │   │
│  │  Any device on  │◄────────────▶│  │  - Cache       │ │   │
│  │  LAN network    │   HTTP       │  │  - Sessions    │ │   │
│  │                 │              │  └────────────────┘ │   │
│  └─────────────────┘              └──────────────────────┘   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Stack Tecnologico

**Frontend:**
- Vue.js 3 (Composition API)
- Tailwind CSS
- Axios per API calls

**Backend:**
- Python 3.11+
- FastAPI (async web framework)
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Pydantic (validation)

**Database & Cache:**
- PostgreSQL 15 (production database)
- Redis 7 (cache & sessions)

**LLM Integration:**
- Ollama (via HTTP API)
- LM Studio (OpenAI-compatible API)

**Container Orchestration:**
- Docker 20.10+
- Docker Compose 2.0+
- Portainer (optional GUI)

**Security Tools Integrati:**
- Nmap (network scanning)
- Bandit (Python SAST)
- Semgrep (multi-language SAST)
- Scapy (packet manipulation)
- Custom modules (wireless, API fuzzing, etc.)

---

## 📋 Requisiti

### Server Sec-Llama

**Hardware Minimo:**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 20 GB SSD
- Network: 100 Mbps

**Hardware Raccomandato:**
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 50+ GB SSD
- Network: 1 Gbps

**Software:**
- Ubuntu 22.04 LTS / Debian 12 (consigliato)
- Docker 20.10+
- Docker Compose 2.0+
- Accesso root/sudo

### Server LLM (PC separato)

**Hardware Minimo (per llama3.1:8b):**
- CPU: 4 cores
- RAM: 16 GB
- GPU: Non necessaria (CPU inference)
- Disk: 10 GB

**Hardware Raccomandato (per modelli grandi):**
- CPU: 8+ cores
- RAM: 64+ GB
- GPU: NVIDIA con 24+ GB VRAM (opzionale ma raccomandato)
- Disk: 100+ GB SSD

**Software:**
- Linux / macOS / Windows
- Ollama OR LM Studio
- Accesso rete LAN

### Network

- ✅ LAN privata (no esposizione Internet diretta)
- ✅ Connettività tra server (firewall configurato)
- ✅ IP statici o DHCP reservation raccomandati

---

## 🚀 Setup Rapido

### 1. Prepara Server LLM

**Opzione A: Ollama (Linux/macOS - Consigliato)**

```bash
# Su server LLM (es. 192.168.1.100)

# 1. Installa Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Configura per accesso rete
sudo mkdir -p /etc/systemd/system/ollama.service.d

sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

# 3. Ricarica e riavvia
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl enable ollama

# 4. Scarica modelli
ollama pull llama3.1:8b        # Veloce (4GB)
ollama pull mistral:latest     # Alternativa
ollama pull codellama:latest   # Per code review

# 5. Verifica
ollama list
curl http://localhost:11434/api/tags

# 6. Configura firewall
sudo ufw allow 11434/tcp
```

**Opzione B: LM Studio (Windows/macOS/Linux - GUI)**

1. Scarica da https://lmstudio.ai/
2. Installa e apri
3. Search → Cerca "llama 3.1" → Download
4. Settings → Server:
   - Host: `0.0.0.0`
   - Port: `1234`
5. Click "Start Server"
6. Firewall: Consenti porta 1234

### 2. Testa Connettività LLM

```bash
# Dal server Sec-Llama (192.168.1.10)

# Test Ollama
curl http://192.168.1.100:11434/api/tags

# Test LM Studio
curl http://192.168.1.100:1234/v1/models

# Se funziona, vedrai JSON con i modelli disponibili
```

### 3. Deploy Sec-Llama

```bash
# Su server Sec-Llama (192.168.1.10)

# 1. Clone repository
git clone https://github.com/yayoboy/Sec-llama.git
cd Sec-llama

# 2. Configura environment
cp .env.example .env
nano .env

# MODIFICA questi valori obbligatori:
# - OLLAMA_HOST=http://192.168.1.100:11434
# - POSTGRES_PASSWORD=TuaPasswordSicura123
# - REDIS_PASSWORD=TuaRedisPassword456
# - SECRET_KEY=$(openssl rand -hex 32)
# - JWT_SECRET_KEY=$(openssl rand -hex 32)
# - ADMIN_PASSWORD=CambiamiAlPrimoLogin!

# 3. Avvia stack
docker-compose up -d

# 4. Verifica stato
docker-compose ps
docker-compose logs -f web-ui

# 5. Accedi alla Web UI
# Browser: http://192.168.1.10:8080
# Login: admin / (password dal .env)
```

---

## ⚙️ Configurazione Dettagliata

### File .env - Parametri Importanti

#### Database

```bash
POSTGRES_DB=sec_llama              # Nome database
POSTGRES_USER=sec_llama            # Username PostgreSQL
POSTGRES_PASSWORD=CHANGE_ME        # Password PostgreSQL (CAMBIARE!)
POSTGRES_PORT=5432                 # Porta esposta (default OK)
```

#### Cache Redis

```bash
REDIS_PASSWORD=CHANGE_ME           # Password Redis (CAMBIARE!)
REDIS_PORT=6379                    # Porta esposta (default OK)
```

#### LLM Provider

```bash
# Provider da usare
LLM_PROVIDER=ollama                # ollama | lm_studio

# Configurazione Ollama
OLLAMA_HOST=http://192.168.1.100:11434
OLLAMA_MODEL=llama3.1:8b           # Modello da usare
OLLAMA_TIMEOUT=120                 # Timeout richieste (secondi)

# Configurazione LM Studio
LM_STUDIO_HOST=http://192.168.1.100:1234
LM_STUDIO_MODEL=local-model
LM_STUDIO_API_KEY=not-needed
```

#### Security

```bash
# Chiavi segrete (GENERARE SEMPRE!)
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Admin di default
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@sec-llama.local
ADMIN_PASSWORD=ChangeMeOnFirstLogin123!
```

#### Application

```bash
DEBUG=false                        # Solo true per development!
LOG_LEVEL=INFO                     # DEBUG | INFO | WARNING | ERROR
WEB_UI_PORT=8080                   # Porta Web UI

# CORS (per production usare dominio specifico)
ALLOWED_ORIGINS=*                  # * per dev, http://domain.com per prod

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100            # Richieste per finestra
RATE_LIMIT_WINDOW=60               # Finestra in secondi
```

### Generare Chiavi Sicure

```bash
# SECRET_KEY (32 bytes hex = 64 caratteri)
openssl rand -hex 32

# JWT_SECRET_KEY (32 bytes hex = 64 caratteri)
openssl rand -hex 32

# Password sicure (16 caratteri alfanumerici)
openssl rand -base64 16
```

---

## 🐳 Deployment Methods

### Metodo 1: Docker Compose (Consigliato per Development)

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild dopo modifiche
docker-compose build --no-cache
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f web-ui

# Restart singolo servizio
docker-compose restart web-ui
```

### Metodo 2: Portainer (Consigliato per Production)

**Installazione Portainer:**

```bash
# Crea volume
docker volume create portainer_data

# Avvia Portainer
docker run -d \
  -p 9000:9000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

# Accedi a https://localhost:9443
# Crea admin user al primo accesso
```

**Deploy via Portainer:**

1. Login a Portainer (https://192.168.1.10:9443)
2. Stacks → Add Stack
3. Nome: `sec-llama`
4. Metodo: Upload
5. Upload: `docker-compose.yml`
6. Environment variables → Advanced mode:
   ```
   POSTGRES_PASSWORD=your_secure_password
   REDIS_PASSWORD=your_redis_password
   OLLAMA_HOST=http://192.168.1.100:11434
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_key
   ADMIN_PASSWORD=YourAdminPass123!
   ```
7. Deploy the stack
8. Verifica status in Containers

**Vantaggi Portainer:**
- ✅ GUI user-friendly
- ✅ Monitoring real-time
- ✅ Log viewer integrato
- ✅ Resource stats (CPU, RAM, network)
- ✅ Easy updates
- ✅ Stack template management

### Metodo 3: Docker Swarm (Production Cluster)

Per deployment multi-node:

```bash
# Inizializza swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml sec-llama

# Status
docker stack ps sec-llama
docker service ls

# Scale service
docker service scale sec-llama_web-ui=3

# Logs
docker service logs -f sec-llama_web-ui

# Remove stack
docker stack rm sec-llama
```

---

## ✅ Verifica e Testing

### Health Checks

```bash
# Web UI health endpoint
curl http://localhost:8080/api/health

# Risposta attesa:
# {"status":"healthy","database":"connected","redis":"connected","llm":"available"}

# PostgreSQL
docker exec sec-llama-postgres pg_isready -U sec_llama

# Redis
docker exec sec-llama-redis redis-cli ping
```

### Test LLM Connection

```bash
# Via Web UI API
curl -X POST http://localhost:8080/api/llm/test \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, are you working?"}'

# Risposta attesa: JSON con response dall'LLM
```

### Test Security Tools

1. **Network Discovery:**
   - Web UI → Tools → Network Discovery
   - Subnet: `192.168.1.0/24`
   - Method: `arp`
   - Execute

2. **Port Scan:**
   - Tools → Port Scan
   - Host: `192.168.1.1`
   - Profile: `standard`
   - Execute

3. **CVE Lookup:**
   - Tools → CVE Lookup
   - CVE ID: `CVE-2024-1234`
   - Search

---

## 🔧 Manutenzione

### Backup Database

```bash
# Backup PostgreSQL
docker exec sec-llama-postgres pg_dump -U sec_llama sec_llama > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20250116.sql | docker exec -i sec-llama-postgres psql -U sec_llama -d sec_llama
```

### Backup Completo

```bash
# Backup volumi Docker
docker run --rm \
  -v sec-llama_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_$(date +%Y%m%d).tar.gz -C /data .

docker run --rm \
  -v sec-llama_redis_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/redis_$(date +%Y%m%d).tar.gz -C /data .
```

### Update Containers

```bash
# Pull nuove immagini
docker-compose pull

# Rebuild e restart
docker-compose up -d --build

# Verifica versioni
docker-compose images
```

### Database Migrations

```bash
# Auto-run al boot via entrypoint.sh
# Per forzare manualmente:

docker exec -it sec-llama-web-ui alembic upgrade head

# Creare nuova migration
docker exec -it sec-llama-web-ui alembic revision --autogenerate -m "Description"
```

### Log Rotation

```bash
# Configurazione Docker log rotation
# In /etc/docker/daemon.json:

{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}

# Restart Docker
sudo systemctl restart docker
```

---

## 🔍 Troubleshooting

### Web UI non accessibile

**Problema:** Browser non carica http://localhost:8080

**Soluzioni:**
```bash
# 1. Verifica container running
docker-compose ps

# 2. Controlla logs
docker-compose logs web-ui

# 3. Verifica porta libera
sudo netstat -tlnp | grep 8080

# 4. Test interno container
docker exec sec-llama-web-ui curl -f http://localhost:8080/api/health

# 5. Verifica firewall
sudo ufw status
sudo ufw allow 8080/tcp
```

### LLM non raggiungibile

**Problema:** Errore "LLM connection failed"

**Soluzioni:**
```bash
# 1. Test connettività da server Sec-Llama
curl http://192.168.1.100:11434/api/tags

# 2. Verifica Ollama running su PC LLM
ssh user@192.168.1.100
systemctl status ollama
sudo systemctl restart ollama

# 3. Verifica firewall su PC LLM
sudo ufw allow 11434/tcp

# 4. Verifica .env
grep OLLAMA_HOST .env

# 5. Rebuild container con nuova config
docker-compose down
docker-compose up -d
```

### Database connection errors

**Problema:** "Database connection failed"

**Soluzioni:**
```bash
# 1. Verifica Postgres healthy
docker-compose ps postgres

# 2. Test connessione
docker exec sec-llama-postgres pg_isready -U sec_llama

# 3. Controlla password
grep POSTGRES_PASSWORD .env

# 4. Reset database (ATTENZIONE: cancella dati!)
docker-compose down
docker volume rm sec-llama_postgres_data
docker-compose up -d

# 5. Verifica migrations
docker exec sec-llama-web-ui alembic current
docker exec sec-llama-web-ui alembic upgrade head
```

### Container crash loop

**Problema:** Container continua a restartare

**Soluzioni:**
```bash
# 1. Vedi logs dettagliati
docker-compose logs --tail=100 web-ui

# 2. Controlla file .env
cat .env | grep -v "^#" | grep -v "^$"

# 3. Verifica permissions
ls -la data/
sudo chown -R 1000:1000 data/

# 4. Rebuild da zero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# 5. Controlla resources
docker stats
```

### High memory usage

**Problema:** Container usa troppa RAM

**Soluzioni:**
```bash
# 1. Limita risorse in docker-compose.yml
services:
  web-ui:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

# 2. Ottimizza workers Uvicorn
# In .env o entrypoint.sh:
WORKERS=2  # Invece di auto-detect

# 3. Configura Redis max memory
services:
  redis:
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

---

## 🔒 Security Best Practices

### 1. Cambia Password di Default

```bash
# Alla prima installazione, cambia:
# - ADMIN_PASSWORD in .env
# - Login via Web UI → Settings → Change Password
```

### 2. Genera Chiavi Sicure

```bash
# Mai usare chiavi di esempio!
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 24)
REDIS_PASSWORD=$(openssl rand -base64 24)
```

### 3. HTTPS in Production

```bash
# Usa reverse proxy (nginx/caddy)
# nginx example:

server {
    listen 443 ssl http2;
    server_name sec-llama.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Firewall Configuration

```bash
# Solo porte necessarie
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp          # SSH
sudo ufw allow 8080/tcp        # Web UI (o 443 se HTTPS)
sudo ufw allow from 192.168.1.0/24 to any port 5432  # PostgreSQL solo da LAN
sudo ufw enable
```

### 5. Network Isolation

```bash
# In docker-compose.yml, usa network separata
networks:
  sec-llama-network:
    driver: bridge
    internal: false  # true se non serve accesso internet
```

### 6. Regular Updates

```bash
# Monthly security updates
docker-compose pull
docker-compose up -d
docker system prune -a --volumes  # Cleanup old images
```

### 7. Audit Logging

Tutti i comandi security sono loggati:
- File: `data/logs/audit.log`
- Database: Tabella `audit_logs`
- Retention: 90 giorni (configurabile)

### 8. Rate Limiting

```bash
# .env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### 9. Backup Encryption

```bash
# Backup con encryption
tar czf - data/ | gpg -c > backup_$(date +%Y%m%d).tar.gz.gpg

# Restore
gpg -d backup_20250116.tar.gz.gpg | tar xzf -
```

---

## 📚 Riferimenti

- **Repository**: https://github.com/yayoboy/Sec-llama
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Features**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Ollama Docs**: https://ollama.com/docs
- **LM Studio**: https://lmstudio.ai
- **Docker Docs**: https://docs.docker.com
- **FastAPI**: https://fastapi.tiangolo.com
- **PostgreSQL**: https://www.postgresql.org/docs

---

**Buon deployment! 🚀🛡️**

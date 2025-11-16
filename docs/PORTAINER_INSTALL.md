# Installazione Sec-Llama in Portainer

Guida completa per deployare Sec-Llama usando Portainer.

## 📋 Prerequisiti

- Portainer installato e funzionante
- Docker Engine configurato
- (Opzionale) Docker Swarm per deployment produzione

## 🎯 Scegli l'Implementazione

Portainer supporta diverse modalità di deployment:

| Implementazione | Metodo Portainer | Complessità |
|----------------|------------------|-------------|
| **mcp-http** | Stack (Compose) | Bassa |
| **web-ui-full** | Stack (Compose) | Media |
| **docker-dev** | Stack (Compose) | Media |
| **docker-production** | Stack (Swarm) | Alta |

---

## 🚀 Metodo 1: Stack Docker Compose (Raccomandato)

### Per: mcp-http, web-ui-full, docker-dev

#### Step 1: Preparare i file

Sul tuo server, clona il repository:

```bash
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama
```

#### Step 2: Scegli implementazione e prepara .env

```bash
# Esempio per web-ui-full
cd implementations/web-ui-full

# Copia e modifica .env
cp .env.example .env
nano .env
```

**Genera password sicure:**
```bash
# Genera SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# Genera POSTGRES_PASSWORD
python3 -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_hex(16))"
```

#### Step 3: Deploy in Portainer

1. **Accedi a Portainer** → http://your-server:9000

2. **Seleziona Environment** (local o remote)

3. **Vai su Stacks** → **Add Stack**

4. **Configurazione Stack:**
   - **Name**: `sec-llama-web-ui` (o altro nome)
   - **Build method**: Scegli **Upload**

5. **Upload docker-compose.yml:**
   - Click su **Upload**
   - Seleziona `docker-compose.yml` dall'implementazione scelta

6. **Environment Variables:**

   Copia il contenuto del tuo `.env` nella sezione **Environment variables**:

   ```
   POSTGRES_DB=sec_llama
   POSTGRES_USER=sec_llama
   POSTGRES_PASSWORD=your-generated-password
   SECRET_KEY=your-generated-secret
   WEB_UI_PORT=8080
   OLLAMA_PORT=11434
   ```

7. **Deploy the stack** → Click **Deploy the stack**

#### Step 4: Verifica Deployment

1. In Portainer, vai su **Stacks** → `sec-llama-web-ui`

2. Verifica che tutti i container siano **running**:
   - ✅ postgres
   - ✅ redis
   - ✅ ollama
   - ✅ web-ui (o mcp-server)

3. **Controlla logs** cliccando sui container

#### Step 5: Pull Modello Ollama

1. Vai su **Containers**
2. Click sul container **ollama**
3. Click su **Console** → **Connect**
4. Esegui:
   ```bash
   ollama pull llama3.1:8b
   ```

5. Oppure via terminale:
   ```bash
   docker exec -it <ollama-container-id> ollama pull llama3.1:8b
   ```

---

## 🏭 Metodo 2: Docker Stack (Swarm) - Produzione

### Per: docker-production

#### Prerequisito: Inizializza Swarm

```bash
# Sul server manager
docker swarm init

# Se hai più nodi, aggiungi worker nodes
docker swarm join-token worker
```

#### Step 1: Abilita Swarm in Portainer

1. In Portainer, vai su **Environments**
2. Seleziona il tuo environment
3. Verifica che **Swarm** sia attivo

#### Step 2: Prepara Stack File

```bash
cd implementations/docker-production

# Prepara .env
cp .env.example .env
nano .env  # Modifica con password sicure
```

#### Step 3: Deploy Stack in Portainer

1. **Stacks** → **Add Stack**

2. **Name**: `sec-llama-production`

3. **Build method**: **Upload**

4. **Upload**: `docker-stack/docker-stack.yml`

5. **Environment Variables**: Copia da `.env`

6. **Deploy the stack**

#### Step 4: Configurazione Secrets (Opzionale)

Per maggiore sicurezza, usa Docker Secrets:

1. **Secrets** → **Add Secret**

2. Crea secrets:
   - `postgres_password`
   - `secret_key`
   - `mcp_api_keys`

3. Modifica `docker-stack.yml` per usare secrets:

```yaml
secrets:
  postgres_password:
    external: true
  secret_key:
    external: true

services:
  web-ui:
    secrets:
      - postgres_password
      - secret_key
```

---

## 🔧 Metodo 3: Git Repository (Consigliato per aggiornamenti)

### Setup Repository in Portainer

#### Step 1: Prepara Repository Git

Assicurati che il repository sia accessibile (pubblico o con credenziali):

```bash
# Repository pubblico
https://github.com/yourusername/Sec-llama.git

# O repository privato con token
https://username:token@github.com/yourusername/Sec-llama.git
```

#### Step 2: Deploy da Git in Portainer

1. **Stacks** → **Add Stack**

2. **Name**: `sec-llama-web-ui`

3. **Build method**: **Repository**

4. **Repository Configuration:**
   - **Repository URL**: `https://github.com/yourusername/Sec-llama.git`
   - **Repository reference**: `main` (o branch specifico)
   - **Compose path**:
     - Per web-ui: `implementations/web-ui-full/docker-compose.yml`
     - Per mcp-http: `implementations/mcp-http/docker-compose.yml`
     - Per docker-dev: `implementations/docker-dev/docker-compose.yml`

5. **Authentication**: Se privato, aggiungi username/token

6. **Environment Variables**: Imposta variabili

7. **Enable automatic updates** (opzionale):
   - ✅ **Automatic updates**
   - Webhook per trigger deploy automatico

8. **Deploy the stack**

#### Vantaggi Git Repository:
- ✅ Aggiornamenti con un click
- ✅ Webhook per auto-deploy
- ✅ Version control
- ✅ Rollback facile

---

## 📊 Accesso alle Applicazioni

### Web UI Full
```
http://your-server:8080
```

### MCP HTTP
```
http://your-server:8765/health
```

### pgAdmin (docker-dev)
```
http://your-server:5050
Email: admin@sec-llama.local
Password: admin (modifica in produzione!)
```

---

## 🔍 Monitoring in Portainer

### Visualizza Logs

1. **Containers** → Seleziona container
2. **Logs** → Visualizza output in real-time
3. Filtra per timestamp, search, etc.

### Resource Usage

1. **Containers** → Overview
2. Vedi CPU, Memory, Network usage
3. Grafici in tempo reale

### Container Stats

1. **Container details** → **Stats**
2. Monitora:
   - CPU %
   - Memory usage
   - Network I/O
   - Block I/O

---

## 🔄 Gestione e Manutenzione

### Aggiornare Stack

#### Da Upload:
1. **Stacks** → Stack name → **Editor**
2. Modifica configurazione
3. **Update the stack**

#### Da Git Repository:
1. **Stacks** → Stack name
2. **Pull and redeploy** → Aggiorna automaticamente

### Riavviare Servizi

1. **Containers** → Seleziona container
2. **Restart** o **Stop/Start**

### Scalare Servizi (Swarm)

1. **Stacks** → Stack name → **Services**
2. Click su servizio
3. **Scale** → Imposta numero repliche
4. **Apply**

### Backup Volumi

1. **Volumes** → Seleziona volume
2. **Export** → Download backup
3. O usa script:
   ```bash
   docker run --rm \
     -v volume_name:/data \
     -v $(pwd):/backup \
     alpine tar czf /backup/volume-backup.tar.gz -C /data .
   ```

---

## 🐛 Troubleshooting

### Container non parte

1. **Containers** → Container → **Logs**
2. Verifica errori
3. **Inspect** → Verifica configurazione
4. Check **Environment variables**

### Porta già in uso

1. Modifica porta in **Environment variables**
2. Update stack
3. O ferma servizio conflittuale

### Database connection errors

1. Verifica container **postgres** running
2. Check logs postgres
3. Verifica **DATABASE_URL** in env variables
4. Test connessione:
   ```bash
   docker exec -it postgres-container psql -U sec_llama
   ```

### Ollama modello mancante

```bash
# Via Portainer Console
docker exec -it ollama-container ollama pull llama3.1:8b

# O via container console in Portainer
ollama pull llama3.1:8b
```

---

## 🔒 Security Best Practices

### 1. Cambia Password Default

Modifica `.env` con password sicure:
```bash
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_hex(16))")
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
MCP_API_KEYS=$(python3 -c "import secrets; print(secrets.token_hex(32))")
```

### 2. Usa Docker Secrets (Swarm)

Invece di environment variables per password:
- Crea Docker Secrets in Portainer
- Referenzia nei servizi

### 3. Network Isolation

In Portainer:
1. **Networks** → Crea network isolata
2. Assegna solo ai container necessari

### 4. Limita Risorse

In stack file:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
```

### 5. HTTPS con Reverse Proxy

Aggiungi Nginx/Traefik come reverse proxy con SSL

---

## 📚 Esempi Configurazione

### Esempio .env per Web UI Full

```bash
# Database
POSTGRES_DB=sec_llama
POSTGRES_USER=sec_llama
POSTGRES_PASSWORD=Xy9mK2nP8qR5sT7u
POSTGRES_PORT=5432

# Redis
REDIS_PORT=6379

# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.1:8b

# Web UI
WEB_UI_PORT=8080
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
DEBUG=false
LOG_LEVEL=INFO
```

### Esempio .env per MCP HTTP

```bash
# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.1:8b

# MCP Server
MCP_PORT=8765
MCP_API_KEYS=9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t9u8v7w6x5y4z3
LOG_LEVEL=INFO
ALLOWED_ORIGINS=*
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=60
```

---

## 🎯 Quick Start Completo in Portainer

### Web UI Full (Più Completo)

```bash
# 1. Clone repo localmente
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama/implementations/web-ui-full

# 2. Prepara .env
cp .env.example .env
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env
python3 -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_hex(16))" >> .env
```

**In Portainer:**
1. Stacks → Add Stack
2. Name: `sec-llama-web`
3. Upload `docker-compose.yml`
4. Paste env variables da `.env`
5. Deploy
6. Console Ollama → `ollama pull llama3.1:8b`
7. Accedi: http://server:8080

### MCP HTTP (Più Semplice)

```bash
# 1. Clone repo
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama/implementations/mcp-http

# 2. Prepara .env
cp .env.example .env
python3 -c "import secrets; print('MCP_API_KEYS=' + secrets.token_hex(32))" >> .env
```

**In Portainer:**
1. Stacks → Add Stack
2. Name: `sec-llama-mcp`
3. Upload `docker-compose.yml`
4. Paste env variables
5. Deploy
6. Console Ollama → `ollama pull llama3.1:8b`
7. Test: `curl http://server:8765/health`

---

## 📞 Supporto

Se hai problemi:
1. Controlla **Logs** in Portainer
2. Verifica **Environment variables**
3. Check **Container status**
4. Vedi [Troubleshooting](#-troubleshooting)

---

**Versione**: 1.0
**Ultimo aggiornamento**: 2025-11-16

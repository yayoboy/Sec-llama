# 🚀 Deploy su Portainer - Guida Rapida

Guida step-by-step per deployare Sec-Llama su Portainer in **5 minuti**.

---

## 📋 Prerequisiti

✅ Portainer installato e funzionante
✅ PC con Ollama/LM Studio sulla LAN
✅ Docker Swarm inizializzato (o standalone mode)

---

## 🎯 Metodo 1: Upload Stack File (Più Semplice)

### Step 1: Prepara l'Immagine Docker

**Prima devi buildare l'immagine Docker localmente:**

```bash
# Sul server con Portainer
cd /path/to/Sec-llama

# Build immagine
docker build -t sec-llama/web-ui:latest -f implementations/lan-server/Dockerfile implementations/lan-server/

# Verifica immagine creata
docker images | grep sec-llama
```

### Step 2: Deploy su Portainer

1. **Accedi a Portainer**: `https://your-server:9443`

2. **Stacks → Add Stack**

3. **Nome Stack**: `sec-llama`

4. **Build Method**: Seleziona "Upload"

5. **Upload File**: Carica `portainer-stack.yml`

6. **Environment Variables**: Click su "Advanced mode" e incolla:

```bash
POSTGRES_PASSWORD=TuaPasswordSicura123
REDIS_PASSWORD=TuaRedisPassword456
OLLAMA_HOST=http://192.168.1.100:11434
SECRET_KEY=chiave_generata_con_openssl_rand_hex_32
JWT_SECRET_KEY=altra_chiave_generata_con_openssl
ADMIN_PASSWORD=CambiamiAlPrimoLogin!
```

**Genera chiavi sicure:**
```bash
# Su terminale
openssl rand -hex 32  # Per SECRET_KEY
openssl rand -hex 32  # Per JWT_SECRET_KEY
```

7. **Deploy the Stack**

8. **Verifica Status**: Tutti i container devono essere "running" (verde)

---

## 🎯 Metodo 2: Repository Git (Automatico)

### Step 1: Setup Repository

Se hai il codice su Git (GitHub, GitLab, etc.):

1. **Stacks → Add Stack**

2. **Nome**: `sec-llama`

3. **Build Method**: Seleziona "Repository"

4. **Repository URL**:
   ```
   https://github.com/yayoboy/Sec-llama.git
   ```

5. **Repository Reference**: `main` (o il tuo branch)

6. **Compose Path**: `portainer-stack.yml`

7. **Environment Variables**: Stesso del Metodo 1

8. **Deploy**

**Vantaggio**: Portainer può auto-update dallo stack quando fai git push!

---

## 🎯 Metodo 3: Web Editor (Manuale)

### Step 1: Crea Stack

1. **Stacks → Add Stack**

2. **Nome**: `sec-llama`

3. **Build Method**: Seleziona "Web editor"

4. **Copia-incolla** il contenuto di `portainer-stack.yml`

5. **Environment Variables**: Aggiungi le variabili (vedi sopra)

6. **Deploy**

---

## ✅ Verifica Deployment

### 1. Controlla Container Status

In Portainer:
- **Stacks** → `sec-llama` → Tutti i servizi devono essere "running"

Container attesi:
- ✅ `sec-llama_postgres` (verde)
- ✅ `sec-llama_redis` (verde)
- ✅ `sec-llama_web-ui` (verde)

### 2. Controlla Logs

Click su ogni container → **Logs**:

**PostgreSQL**:
```
database system is ready to accept connections
```

**Redis**:
```
Ready to accept connections
```

**Web UI**:
```
Application startup complete
Uvicorn running on http://0.0.0.0:8080
```

### 3. Test Health Endpoint

Da terminale o Portainer Console:

```bash
curl http://localhost:8080/api/health
```

Risposta attesa:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "llm": "available"
}
```

### 4. Accedi alla Web UI

Apri browser:
```
http://your-server-ip:8080
```

Login:
- Username: `admin`
- Password: (quella impostata in `ADMIN_PASSWORD`)

---

## 🔧 Configurazioni Avanzate

### Auto-Restart Policy

Il stack è già configurato con:
```yaml
deploy:
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
```

### Resource Limits

Configurato per production:

**PostgreSQL**:
- Memory: 1GB limit, 512MB reservation

**Redis**:
- Memory: 512MB limit, 256MB reservation

**Web UI**:
- Memory: 2GB limit, 1GB reservation
- CPU: 2 cores limit, 1 core reservation

### Modifica Resource Limits

In `portainer-stack.yml`, sezione `deploy.resources`:

```yaml
deploy:
  resources:
    limits:
      memory: 4G      # Aumenta se necessario
      cpus: '4.0'
    reservations:
      memory: 2G
      cpus: '2.0'
```

---

## 📊 Monitoring in Portainer

### 1. Resource Stats

**Stacks** → `sec-llama` → Click su container:
- CPU usage
- Memory usage
- Network I/O
- Disk I/O

### 2. Logs Real-time

Click su container → **Logs** → Abilita "Auto-refresh"

### 3. Exec Console

Per debug:
1. Click su `sec-llama_web-ui`
2. **Console** → `/bin/sh`
3. Esegui comandi:
   ```bash
   # Test database
   alembic current

   # Test LLM
   curl $OLLAMA_HOST/api/tags
   ```

---

## 🔄 Update Stack

### Metodo 1: Re-deploy

1. **Stacks** → `sec-llama` → **Editor**
2. Modifica `portainer-stack.yml`
3. **Update the stack**

### Metodo 2: Pull New Image

Se usi immagini da registry:

1. **Images** → Cerca `sec-llama/web-ui`
2. **Pull image**
3. **Stacks** → `sec-llama` → **Update**

---

## 🔒 Security in Portainer

### 1. Network Isolation

Stack usa rete overlay dedicata:
```yaml
networks:
  sec-llama-network:
    driver: overlay
    attachable: true
```

### 2. Secrets Management

**Usa Portainer Secrets per production:**

1. **Secrets** → **Add secret**
   - Name: `postgres_password`
   - Secret: `your-secure-password`

2. Modifica stack:
   ```yaml
   services:
     postgres:
       secrets:
         - postgres_password
       environment:
         POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
   ```

### 3. Access Control

**Settings** → **Users**:
- Crea utenti con permessi limitati
- Assegna team agli stack
- Audit log abilitato

---

## 🐛 Troubleshooting

### Container Non Si Avvia

**Problema**: Container in stato "error" o "starting"

**Soluzione**:
1. Click su container → **Logs**
2. Controlla errori
3. Verifica environment variables
4. Check image pullata correttamente

### Database Connection Failed

**Problema**: Web UI non si connette a PostgreSQL

**Soluzione**:
```bash
# Console su web-ui container
echo $DATABASE_URL

# Verifica Postgres running
docker exec sec-llama_postgres pg_isready
```

### LLM Non Raggiungibile

**Problema**: "LLM connection failed"

**Soluzione**:
```bash
# Console su web-ui container
curl $OLLAMA_HOST/api/tags

# Se fallisce, verifica:
# 1. IP corretto in OLLAMA_HOST
# 2. Ollama running su PC remoto
# 3. Firewall aperto porta 11434
```

### Porta 8080 Occupata

**Problema**: "Port 8080 already in use"

**Soluzione**:
1. Environment variables → Aggiungi:
   ```
   WEB_UI_PORT=8081
   ```
2. Update stack

---

## 🔄 Backup & Restore

### Backup Volumes

**In Portainer:**

1. **Volumes** → Seleziona volume
2. **Export** → Download

**Via CLI:**
```bash
# Backup PostgreSQL volume
docker run --rm \
  -v sec-llama_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_$(date +%Y%m%d).tar.gz -C /data .
```

### Restore Volumes

1. **Volumes** → **Import**
2. Upload backup file
3. Restart stack

---

## 📈 Scaling

### Aumenta Replicas

**Per high-availability:**

1. Modifica stack:
   ```yaml
   services:
     web-ui:
       deploy:
         replicas: 3  # Aumenta da 1 a 3
   ```

2. **Update stack**

Portainer bilancerà automaticamente il traffico.

### Load Balancer

Aggiungi HAProxy/Nginx davanti:

```yaml
services:
  loadbalancer:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

---

## 📚 Riferimenti

- **Portainer Docs**: https://docs.portainer.io/
- **Docker Swarm**: https://docs.docker.com/engine/swarm/
- **Stack File Reference**: `portainer-stack.yml`
- **Environment Template**: `portainer-env.txt`
- **Deployment Guide**: `DEPLOYMENT.md`

---

**Buon deploy su Portainer! 🚀**

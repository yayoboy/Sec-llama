# 🚀 Guida Deployment - Sec-Llama LAN Server

Guida completa per il deployment su server Ubuntu/Debian con Portainer e LLM remoto.

---

## 📋 Prerequisiti Verificati

- ✅ Server Ubuntu/Debian
- ✅ Docker già installato
- ✅ Portainer per deployment
- ✅ LLM su PC separato (Ollama o LM Studio)

---

## 🎯 Architettura Deploy

```
┌─────────────────────────────────────────┐
│          Rete LAN                       │
│                                         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │ PC LLM       │  │ Server          │ │
│  │              │  │                 │ │
│  │ Ollama       │←→│ Sec-Llama      │ │
│  │ :11434       │  │ Portainer :9000│ │
│  │              │  │ Web UI :8080   │ │
│  └──────────────┘  └─────────────────┘ │
│  192.168.1.100     192.168.1.10       │
└─────────────────────────────────────────┘
```

---

## STEP 1: Configurare Server LLM Remoto

### Su PC con Ollama (192.168.1.100)

**1.1. Installa Ollama (se non già installato)**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**1.2. Configura accesso rete**

Ollama di default ascolta solo su localhost. Devi configurarlo per accesso LAN:

```bash
# Metodo 1: Systemd service (RACCOMANDATO - persistente)
sudo mkdir -p /etc/systemd/system/ollama.service.d

# Crea override file
sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

# Ricarica e riavvia
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Verifica
sudo systemctl status ollama
```

**1.3. Scarica un modello**
```bash
# Modello leggero per iniziare (4GB RAM)
ollama pull llama3.1:8b

# Oppure modello più potente (richiede ~64GB RAM)
# ollama pull llama3.1:70b

# Verifica modelli scaricati
ollama list
```

**1.4. Testa il server**
```bash
# Dal PC Ollama stesso
curl http://localhost:11434/api/tags

# Dovresti vedere output JSON con i modelli
```

**1.5. Configura firewall sul PC Ollama**
```bash
# Ubuntu/Debian
sudo ufw allow 11434/tcp
sudo ufw status

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --reload
```

**1.6. Testa da server Sec-Llama**
```bash
# Dal server Sec-Llama (192.168.1.10)
# Sostituisci 192.168.1.100 con IP del tuo PC Ollama
curl http://192.168.1.100:11434/api/tags

# Se funziona, dovresti vedere i modelli
# Se non funziona, verifica:
# - Firewall su PC Ollama
# - Connettività rete: ping 192.168.1.100
```

---

## STEP 2: Preparare Server Sec-Llama

### Su Server (192.168.1.10)

**2.1. Verifica Docker e Portainer**
```bash
# Verifica Docker
docker --version
docker-compose --version

# Verifica Portainer (se già installato)
docker ps | grep portainer

# Se Portainer NON è installato:
docker volume create portainer_data

docker run -d \
  -p 9000:9000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

# Accedi a Portainer: http://192.168.1.10:9000
# Crea admin user alla prima configurazione
```

**2.2. Clona repository sul server**
```bash
# Vai nella directory home o dove preferisci
cd ~

# Clona repository
git clone https://github.com/yayoboy/Sec-llama.git

# Entra nella directory
cd Sec-llama/implementations/lan-server

# Verifica contenuto
ls -la
```

**2.3. Prepara file di configurazione**
```bash
# Copia template environment
cp .env.example .env

# Modifica .env con i tuoi parametri
nano .env
```

**2.4. Configura .env**

**IMPORTANTE:** Modifica questi valori nel file `.env`:

```bash
# ===== LLM Configuration =====
LLM_PROVIDER=ollama
OLLAMA_HOST=http://192.168.1.100:11434    # ← IP del tuo PC Ollama
OLLAMA_MODEL=llama3.1:8b                   # ← Modello che hai scaricato
OLLAMA_TIMEOUT=120

# ===== Security Keys (GENERA NUOVE!) =====
# Genera con: openssl rand -base64 32
SECRET_KEY=GENERA-UNA-STRINGA-RANDOM-32-CARATTERI
JWT_SECRET_KEY=GENERA-ALTRA-STRINGA-RANDOM-32-CARATTERI

# ===== Database =====
POSTGRES_DB=sec_llama
POSTGRES_USER=sec_llama
POSTGRES_PASSWORD=scegli-password-sicura-qui      # ← Cambia!
POSTGRES_PORT=5432

# ===== Redis =====
REDIS_PORT=6379
REDIS_PASSWORD=scegli-password-redis-sicura       # ← Cambia!

# ===== Web UI =====
WEB_UI_PORT=8080

# ===== CORS =====
ALLOWED_ORIGINS=*    # Per produzione usa domini specifici

# ===== Rate Limiting =====
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

**2.5. Genera chiavi sicure**
```bash
# Genera SECRET_KEY
echo "SECRET_KEY=$(openssl rand -base64 32)"

# Genera JWT_SECRET_KEY
echo "JWT_SECRET_KEY=$(openssl rand -base64 32)"

# Copia questi valori nel file .env
```

**2.6. Salva .env**
```bash
# Dopo aver modificato .env
# Premi Ctrl+O per salvare
# Premi Ctrl+X per uscire da nano

# Verifica configurazione
cat .env | grep -E "OLLAMA_HOST|SECRET_KEY|POSTGRES_PASSWORD|REDIS_PASSWORD"
```

---

## STEP 3: Deploy con Portainer

### 3.1. Accedi a Portainer

Apri browser e vai a:
```
http://192.168.1.10:9000
```

Login con le credenziali admin create durante setup.

### 3.2. Crea Stack

**1. Nel menu laterale:** Clicca su **Stacks**

**2. Clicca:** **Add stack** (pulsante in alto a destra)

**3. Configura lo stack:**

**Name:**
```
sec-llama
```

**Build method:** Seleziona **Web editor**

**4. Copia contenuto file stack:**

Nel campo Web editor, incolla il contenuto di `portainer-stack.yml`:

```bash
# Sul server, visualizza il contenuto
cat ~/Sec-llama/implementations/lan-server/portainer-stack.yml
```

Copia tutto e incolla nell'editor di Portainer.

**5. Aggiungi Environment Variables:**

Scorri in basso fino a **Environment variables**.

Clicca su **Advanced mode** (interruttore in alto a destra).

Incolla queste variabili (MODIFICA I VALORI):

```env
IMAGE_TAG=latest
WEB_UI_PORT=8080
LOG_LEVEL=INFO

# SECURITY - CHANGE THESE!
SECRET_KEY=tua-secret-key-generata
JWT_SECRET_KEY=tua-jwt-secret-key-generata
POSTGRES_PASSWORD=tua-password-postgres
REDIS_PASSWORD=tua-password-redis

# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_HOST=http://192.168.1.100:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TIMEOUT=120

# LM Studio (se usi LM Studio invece di Ollama)
# LLM_PROVIDER=lm-studio
# LM_STUDIO_HOST=http://192.168.1.100:1234
# LM_STUDIO_MODEL=local-model
# LM_STUDIO_API_KEY=not-needed

# CORS
ALLOWED_ORIGINS=*

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

**IMPORTANTE:** Usa i valori che hai generato in `.env`!

**6. Deploy Stack:**

Clicca **Deploy the stack** in fondo alla pagina.

Portainer inizierà a:
- Creare i container (PostgreSQL, Redis, Web UI)
- Configurare la rete
- Montare i volumi

---

## STEP 4: Verifica Deployment

### 4.1. Controlla stato containers

In Portainer:
1. Vai a **Containers** nel menu laterale
2. Dovresti vedere 3 container in stato **running**:
   - `sec-llama_postgres`
   - `sec-llama_redis`
   - `sec-llama_web-ui`

Se qualche container è in stato **unhealthy** o **stopped**:

**Visualizza logs:**
- Clicca sul nome del container
- Vai su tab **Logs**
- Leggi gli errori

**Problemi comuni:**
- **postgres**: Password errata in env variables
- **redis**: Password errata
- **web-ui**: Non riesce a connettersi a postgres/redis/ollama

### 4.2. Testa connessione LLM

Dal server Sec-Llama:
```bash
# Testa connessione a Ollama
curl http://192.168.1.100:11434/api/tags

# Se funziona, dovresti vedere JSON con modelli
```

### 4.3. Accedi alla Web UI

Apri browser:
```
http://192.168.1.10:8080
```

Dovresti vedere la **Sec-Llama Web UI**!

### 4.4. Configura AI nella Web UI

1. **Accedi alla Web UI**: `http://192.168.1.10:8080`

2. **Vai a AI Configuration** (nel menu)

3. **Configura LLM:**
   - Provider: `Ollama` (o `LM Studio`)
   - Host: `http://192.168.1.100:11434`
   - Model: `llama3.1:8b`

4. **Clicca Test Connection**
   - Dovresti vedere: ✅ Connection successful
   - Lista modelli disponibili

5. **Clicca Save Configuration**

### 4.5. Health Check

Verifica health dello stack:
```bash
# Da terminale server
curl http://localhost:8080/api/health

# Dovresti vedere JSON:
# {
#   "status": "healthy",
#   "services": {
#     "api": "healthy",
#     "database": "healthy",
#     "redis": "healthy",
#     "llm": "ok"
#   }
# }
```

---

## STEP 5: Test Funzionalità

### 5.1. Test Network Discovery

Dalla Web UI:
1. Vai a **Tools** → **Network Security**
2. Seleziona **Host Discovery**
3. Inserisci: `192.168.1.0/24` (tua rete)
4. Clicca **Scan**
5. Attendi risultati con analisi AI

### 5.2. Test CVE Lookup

1. Vai a **Tools** → **Threat Intelligence**
2. Seleziona **CVE Lookup**
3. Inserisci: `CVE-2024-21413` (esempio)
4. Clicca **Analyze**
5. Dovresti vedere analisi AI del CVE

---

## 🔧 Gestione Stack

### Visualizzare Logs
```bash
# Da Portainer UI
Containers → Click sul container → Tab "Logs"

# Da CLI
docker logs sec-llama_web-ui
docker logs sec-llama_postgres
docker logs sec-llama_redis
```

### Riavviare Stack
```bash
# Da Portainer UI
Stacks → sec-llama → Actions → Restart

# Da CLI
cd ~/Sec-llama/implementations/lan-server
docker-compose restart
```

### Aggiornare Stack
```bash
# 1. Pull nuove immagini
git pull origin main
cd implementations/lan-server

# 2. Da Portainer UI
Stacks → sec-llama → Editor
# Modifica se necessario
# Clicca "Update the stack"

# 3. Da CLI
docker-compose pull
docker-compose up -d
```

### Stop Stack
```bash
# Da Portainer UI
Stacks → sec-llama → Actions → Stop

# Da CLI
docker-compose down
```

### Remove Stack (ATTENZIONE: elimina volumi!)
```bash
# Da Portainer UI
Stacks → sec-llama → Actions → Remove
# Seleziona "Remove associated volumes" se vuoi eliminare dati

# Da CLI
docker-compose down -v  # -v elimina volumi!
```

---

## 🔒 Configurazione Firewall Server

Configura firewall sul server Sec-Llama:

```bash
# Abilita UFW se non già fatto
sudo ufw enable

# Permetti SSH (IMPORTANTE - non bloccarti fuori!)
sudo ufw allow ssh
sudo ufw allow 22/tcp

# Permetti Portainer
sudo ufw allow 9000/tcp
sudo ufw allow 9443/tcp

# Permetti Web UI
sudo ufw allow 8080/tcp

# (Opzionale) Permetti PostgreSQL solo da LAN
sudo ufw allow from 192.168.1.0/24 to any port 5432

# (Opzionale) Permetti Redis solo da LAN
sudo ufw allow from 192.168.1.0/24 to any port 6379

# Verifica regole
sudo ufw status

# Output dovrebbe mostrare:
# To                         Action      From
# --                         ------      ----
# 22/tcp                     ALLOW       Anywhere
# 9000/tcp                   ALLOW       Anywhere
# 8080/tcp                   ALLOW       Anywhere
```

---

## 🔐 Security Hardening (Produzione)

### 1. Setup HTTPS con Nginx Reverse Proxy

**Installa Nginx:**
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y
```

**Configura Nginx:**
```bash
sudo nano /etc/nginx/sites-available/sec-llama
```

```nginx
server {
    listen 80;
    server_name sec-llama.tuodominio.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name sec-llama.tuodominio.com;

    # SSL Certificate (configurato da certbot)
    ssl_certificate /etc/letsencrypt/live/sec-llama.tuodominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sec-llama.tuodominio.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Proxy to Sec-Llama
    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://localhost:8080/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**Abilita configurazione:**
```bash
sudo ln -s /etc/nginx/sites-available/sec-llama /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Ottieni certificato SSL:**
```bash
sudo certbot --nginx -d sec-llama.tuodominio.com
```

### 2. Configura Backup Automatici

```bash
# Crea directory backup
sudo mkdir -p /backup/sec-llama

# Crea script backup
sudo nano /usr/local/bin/backup-sec-llama.sh
```

```bash
#!/bin/bash
# Backup Sec-Llama Database

BACKUP_DIR="/backup/sec-llama"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER="sec-llama_postgres"

# Backup PostgreSQL
docker exec $CONTAINER pg_dump -U sec_llama sec_llama | gzip > "$BACKUP_DIR/sec-llama-db_$TIMESTAMP.sql.gz"

# Rimuovi backup più vecchi di 30 giorni
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completato: $BACKUP_DIR/sec-llama-db_$TIMESTAMP.sql.gz"
```

```bash
# Rendi eseguibile
sudo chmod +x /usr/local/bin/backup-sec-llama.sh

# Aggiungi a crontab (backup giornaliero alle 2 AM)
sudo crontab -e

# Aggiungi questa riga:
0 2 * * * /usr/local/bin/backup-sec-llama.sh >> /var/log/sec-llama-backup.log 2>&1
```

### 3. Monitoring

**Setup Prometheus + Grafana (opzionale):**
```bash
# Aggiungi al docker-compose.yml o come stack separato
# Vedi: https://prometheus.io/docs/guides/docker-compose/
```

---

## 🐛 Troubleshooting

### Web UI non accessibile

```bash
# 1. Verifica container running
docker ps | grep sec-llama

# 2. Verifica logs
docker logs sec-llama_web-ui

# 3. Verifica porta
sudo netstat -tulpn | grep 8080

# 4. Verifica health
curl http://localhost:8080/api/health
```

### LLM non raggiungibile

```bash
# 1. Testa da server
curl http://192.168.1.100:11434/api/tags

# 2. Testa connettività
ping 192.168.1.100

# 3. Verifica firewall PC Ollama
# Sul PC Ollama:
sudo ufw status | grep 11434

# 4. Verifica Ollama running
# Sul PC Ollama:
sudo systemctl status ollama
```

### Database errors

```bash
# 1. Verifica password in env variables
cat .env | grep POSTGRES_PASSWORD

# 2. Logs PostgreSQL
docker logs sec-llama_postgres

# 3. Test connessione diretta
docker exec -it sec-llama_postgres psql -U sec_llama -d sec_llama
```

### Out of memory

```bash
# 1. Verifica risorse
docker stats

# 2. Se necessario, limita risorse nel docker-compose.yml
# Aggiungi sotto ogni servizio:
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
```

---

## 📞 Support

- **Logs**: `docker logs <container-name>`
- **Health**: `curl http://localhost:8080/api/health`
- **Documentation**: `~/Sec-llama/implementations/lan-server/README.md`

---

**Deployment completato! 🎉**

Accedi a: `http://192.168.1.10:8080` (o `https://sec-llama.tuodominio.com` se hai configurato HTTPS)

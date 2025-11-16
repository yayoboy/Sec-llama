# ⚡ Quick Start - Sec-Llama

Guida rapida per il deployment in **5 minuti**.

---

## 📋 Prerequisiti

Prima di iniziare, assicurati di avere:

- ✅ **Docker** 20.10+ installato
- ✅ **Docker Compose** 2.0+ installato
- ✅ **PC con LLM** sulla stessa rete LAN (Ollama o LM Studio)

---

## 🚀 Step 1: Configura LLM Server

### Opzione A: Ollama (Consigliato)

Sul PC che ospiterà l'LLM (es. `192.168.1.100`):

```bash
# 1. Installa Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Configura accesso rete
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

# 3. Riavvia servizio
sudo systemctl daemon-reload
sudo systemctl restart ollama

# 4. Scarica modello
ollama pull llama3.1:8b

# 5. Verifica
curl http://localhost:11434/api/tags
```

### Opzione B: LM Studio

1. Scarica da [https://lmstudio.ai/](https://lmstudio.ai/)
2. Carica un modello (es. Llama 3.1 8B)
3. Settings → Server → Host: `0.0.0.0`, Port: `1234`
4. Click "Start Server"

---

## 🛠️ Step 2: Deploy Sec-Llama

Sul server che ospiterà Sec-Llama (es. `192.168.1.10`):

```bash
# 1. Clone repository (o trasferisci i file)
git clone https://github.com/yayoboy/Sec-llama.git
cd Sec-llama

# 2. Copia configurazione
cp .env.example .env

# 3. Modifica .env
nano .env
```

**Valori OBBLIGATORI da modificare in `.env`:**

```bash
# Indirizzo del PC con Ollama/LM Studio
OLLAMA_HOST=http://192.168.1.100:11434

# Password sicure
POSTGRES_PASSWORD=TuaPasswordSicura123!
REDIS_PASSWORD=TuaRedisPassword456!

# Chiavi segrete (genera con: openssl rand -hex 32)
SECRET_KEY=chiave_random_32_caratteri_qui
JWT_SECRET_KEY=altra_chiave_random_32_caratteri

# Password admin (CAMBIALA AL PRIMO LOGIN!)
ADMIN_PASSWORD=ChangeMeOnFirstLogin123!
```

```bash
# 4. Avvia i container
docker-compose up -d

# 5. Verifica stato
docker-compose ps

# 6. Segui i log
docker-compose logs -f web-ui
```

---

## 🌐 Step 3: Accedi alla Web UI

Apri il browser e vai a:

```
http://192.168.1.10:8080
```

**Credenziali di default:**
- Username: `admin`
- Password: quella impostata in `.env` (default: `ChangeMeOnFirstLogin123!`)

**⚠️ IMPORTANTE:** Cambia la password immediatamente dopo il primo login!

---

## ✅ Verifica Funzionamento

### Test Connessione LLM

```bash
# Dal server Sec-Llama
curl http://192.168.1.100:11434/api/tags

# Dovresti vedere JSON con i modelli disponibili
```

### Test Database

```bash
# Controlla che Postgres sia up
docker exec sec-llama-postgres pg_isready -U sec_llama

# Output: /var/run/postgresql:5432 - accepting connections
```

### Test Web UI

```bash
# Controlla health endpoint
curl http://localhost:8080/api/health

# Output: {"status":"healthy",...}
```

---

## 📊 Comandi Utili

```bash
# Vedere tutti i container
docker-compose ps

# Seguire i log
docker-compose logs -f

# Riavviare un servizio
docker-compose restart web-ui

# Fermare tutto
docker-compose down

# Fermare e rimuovere volumi (ATTENZIONE: cancella il database!)
docker-compose down -v

# Aggiornare i container
docker-compose pull
docker-compose up -d
```

---

## 🔧 Troubleshooting

### 1. LLM non raggiungibile

```bash
# Verifica firewall sul PC LLM
sudo ufw allow 11434/tcp  # Per Ollama
sudo ufw allow 1234/tcp   # Per LM Studio

# Testa connettività
ping 192.168.1.100
telnet 192.168.1.100 11434
```

### 2. Container non si avvia

```bash
# Controlla logs dettagliati
docker-compose logs web-ui

# Verifica file .env
cat .env | grep -v "^#" | grep -v "^$"

# Rebuilda container
docker-compose build --no-cache web-ui
docker-compose up -d
```

### 3. Database connection error

```bash
# Verifica che Postgres sia healthy
docker-compose ps postgres

# Controlla password in .env
grep POSTGRES_PASSWORD .env

# Reset database (ATTENZIONE: cancella dati!)
docker-compose down
docker volume rm sec-llama_postgres_data
docker-compose up -d
```

### 4. Porta 8080 già in uso

Modifica `.env`:
```bash
WEB_UI_PORT=8081  # O un'altra porta libera
```

Riavvia:
```bash
docker-compose down
docker-compose up -d
```

---

## 🎯 Prossimi Passi

1. **Cambia password admin** nella Web UI
2. **Configura API keys** per servizi esterni
3. **Testa gli strumenti** di scanning
4. **Leggi la documentazione completa** in `implementations/lan-server/DEPLOY_GUIDE.md`

---

## 📚 Documentazione Completa

- **Deployment Dettagliato**: `implementations/lan-server/DEPLOY_GUIDE.md`
- **Configurazione Avanzata**: `implementations/lan-server/.env.example`
- **Architettura**: `README.md`
- **Features**: `IMPLEMENTATION_SUMMARY.md`

---

## 🆘 Supporto

Per problemi o domande:

1. Controlla i logs: `docker-compose logs -f`
2. Verifica la configurazione: `cat .env`
3. Consulta la guida completa in `implementations/lan-server/DEPLOY_GUIDE.md`

---

**Buon security testing! 🛡️**

# Docker Production - Deploy Production-Ready

Stack Docker Swarm completo per produzione con tutti i servizi.

## 🚀 Installazione Rapida

```bash
./install.sh
```

Questo comando:
- ✅ Verifica prerequisiti
- ✅ Inizializza Docker Swarm
- ✅ Genera password sicure
- ✅ Crea secrets Docker
- ✅ Build immagini
- ✅ Deploy stack completo
- ✅ Configura backup automatici (opzionale)

## 📦 Servizi Inclusi

- **PostgreSQL**: Database production
- **Redis**: Cache e sessions
- **Ollama**: LLM server
- **MCP Server**: Tool server
- **Web UI**: Interfaccia web
- **Nginx**: Reverse proxy (opzionale)
- **Backup**: Backup automatici (opzionale)

## ⚙️ Configurazione

### Opzioni Installazione

```bash
# Installazione base
./install.sh

# Con Nginx reverse proxy
./install.sh --with-nginx

# Con backup automatici
./install.sh --with-backup

# Tutto insieme
./install.sh --with-nginx --with-backup --stack-name production
```

### Configurare Ollama Remoto

Dopo l'installazione, vai su:
**http://localhost:8080/ai-config**

E configura il tuo server Ollama remoto.

## 🔧 Gestione Stack

### Visualizza Servizi
```bash
docker stack services sec-llama
```

### Logs
```bash
docker service logs -f sec-llama_web-ui
docker service logs -f sec-llama_mcp-server
```

### Scaling
```bash
# Scala Web UI a 3 repliche
docker service scale sec-llama_web-ui=3

# Scala MCP Server a 2 repliche
docker service scale sec-llama_mcp-server=2
```

### Update
```bash
# Rebuild immagini
./build.sh

# Update stack (zero downtime)
docker stack deploy -c docker-stack.yml sec-llama
```

### Rimozione
```bash
./uninstall.sh
```

## 📊 Accesso

- **Web UI**: http://localhost:8080
- **MCP Server**: http://localhost:8765
- **Ollama**: http://localhost:11434
- **Nginx** (se abilitato): https://localhost

## 🔒 Sicurezza

### Credenziali

Le credenziali sono generate automaticamente e salvate in `.env`:

```bash
cat .env
```

### Cambiare Password

```bash
nano .env
# Modifica POSTGRES_PASSWORD, REDIS_PASSWORD, SECRET_KEY

# Ricarica secrets
./reload-secrets.sh

# Redeploy
docker stack deploy -c docker-stack.yml sec-llama
```

### HTTPS con Nginx

```bash
# Genera certificati
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Deploy con Nginx
./install.sh --with-nginx
```

## 🔄 Backup e Restore

### Backup Manuale

```bash
./backup.sh
```

### Restore

```bash
./restore.sh backup_TIMESTAMP.tar.gz
```

### Backup Automatici

Se installato con `--with-backup`, i backup vengono eseguiti automaticamente ogni notte alle 2 AM.

Backup salvati in: `./backups/`

## 📈 Monitoring

### Health Checks

```bash
# Web UI
curl http://localhost:8080/health

# MCP Server
curl http://localhost:8765/health

# Ollama
curl http://localhost:11434/api/tags
```

### Stato Servizi

```bash
docker service ps sec-llama_web-ui
docker service ps sec-llama_mcp-server
```

## 🌐 High Availability

### Multi-Node Setup

```bash
# Sul manager node
docker swarm init --advertise-addr MANAGER_IP

# Sui worker nodes
docker swarm join --token TOKEN MANAGER_IP:2377

# Deploy su cluster
docker stack deploy -c docker-stack.yml sec-llama
```

I servizi verranno distribuiti automaticamente sui nodi disponibili.

## 🆘 Troubleshooting

### Servizio Non Parte

```bash
# Visualizza errori
docker service ps sec-llama_web-ui --no-trunc

# Logs dettagliati
docker service logs --tail 100 sec-llama_web-ui

# Restart forzato
docker service update --force sec-llama_web-ui
```

### Ollama Non Si Connette

1. Verifica Ollama running:
```bash
docker service logs sec-llama_ollama
curl http://localhost:11434/api/tags
```

2. Configura in Web UI:
http://localhost:8080/ai-config

### Database Issues

```bash
# Connettiti al database
docker exec -it $(docker ps -q -f name=sec-llama_postgres) \
  psql -U sec_llama -d sec_llama

# Backup database
./backup.sh
```

## 📚 Documentazione Completa

Vedi: [DOCKER_STACK_INSTALLATION.md](../../docs/DOCKER_STACK_INSTALLATION.md)

## 🎯 Prossimi Passi

Dopo l'installazione:

1. ✅ Configura AI: http://localhost:8080/ai-config
2. ✅ Crea API Keys: http://localhost:8080/api-keys
3. ✅ Esplora Tools: http://localhost:8080/tools
4. ✅ Configura HTTPS (produzione)
5. ✅ Setup backup automatici

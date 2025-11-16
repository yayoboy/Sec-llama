# 🚀 Sec-Llama - Quick Start Guide

La suite di sicurezza informatica più completa con IA locale.

---

## ⚡ Installazione Rapida (1 Comando)

```bash
# Clone del repository
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Installazione completa con Docker Stack
./scripts/install_stack.sh

# Fatto! 🎉
# Accedi a: http://localhost:8080
```

---

## 🎯 Cosa Otterrai

### ✅ Sistema Completo Pre-Configurato

- **PostgreSQL**: Database production-ready
- **Redis**: Cache e session management
- **Ollama**: LLM locale per analisi IA
- **MCP Server**: Server di tool di sicurezza
- **Web UI**: Interfaccia web moderna
- **Nginx**: Reverse proxy (opzionale)
- **Backup**: Sistema di backup automatico (opzionale)

### ✅ Interfaccia Web Completa

Accedi a **http://localhost:8080** e troverai:

1. **Dashboard**: Statistiche real-time, esecuzioni recenti, grafici
2. **Tools**: Esecuzione tool di sicurezza con form dinamici
3. **AI Configuration**: ⭐ **NUOVO!** Configurazione IA completa
4. **Configuration**: Editor YAML con validazione
5. **API Keys**: Gestione chiavi API con tracking
6. **Audit Logs**: Visualizzatore log con export

---

## 🤖 Configurazione IA (Nuova Funzionalità!)

### Configurare Ollama Remoto

1. **Vai su**: http://localhost:8080/ai-config
2. **Configura Ollama Host**:
   - Locale: `http://localhost:11434`
   - Remoto: `http://192.168.1.100:11434`
   - Server LAN: `http://server-ia.local:11434`
3. **Testa Connessione**: Verifica connettività e latenza
4. **Gestisci Modelli**:
   - Visualizza modelli installati
   - Scarica nuovi modelli (es. `llama3.1:8b`, `mixtral:8x7b`)
   - Testa generazione
   - Elimina modelli non utilizzati

### Configurare Server IA Separato

**Sul Server IA (Macchina Remota)**:
```bash
# Installa Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Configura per accesso remoto
export OLLAMA_HOST=0.0.0.0:11434

# Avvia Ollama
ollama serve
```

**Nella Web UI di Sec-Llama**:
1. Vai su **AI Configuration**
2. Imposta **Ollama Host**: `http://IP_SERVER:11434`
3. Clicca **Test Connection**
4. **Save Configuration**

---

## 📊 Funzionalità Principali

### 1. Tool di Sicurezza

- **Network Discovery**: Scoperta host nella rete locale
- **Port Scanning**: Scansione porte con analisi IA
- **Vulnerability Scanning**: Analisi vulnerabilità
- **Code Analysis**: SAST per analisi codice
- **Threat Intelligence**: Lookup CVE e MITRE ATT&CK
- **Web Security**: Analisi sicurezza web applicazioni

### 2. Gestione IA

- ✅ Configurazione Ollama locale/remoto
- ✅ Gestione modelli (pull, delete, info)
- ✅ Test connessione con latency
- ✅ Test generazione con risultati
- ✅ Selezione modello default
- ✅ Configurazione parametri (temperature, max_tokens)
- ✅ Stato AI real-time

### 3. API MCP

Accesso programmatico via MCP Protocol:
- **Locale**: Stdio transport per Claude Desktop
- **Remoto**: HTTP/SSE transport per LAN

### 4. Scalabilità

```bash
# Scala Web UI a 3 repliche
docker service scale sec-llama_web-ui=3

# Scala MCP Server a 2 repliche
docker service scale sec-llama_mcp-server=2
```

---

## 🔧 Comandi Utili

### Gestione Stack

```bash
# Visualizza servizi
docker stack services sec-llama

# Visualizza logs
docker service logs -f sec-llama_web-ui

# Riavvia servizio
docker service update --force sec-llama_web-ui

# Rimuovi stack
docker stack rm sec-llama
```

### Gestione Modelli IA

```bash
# Lista modelli
curl http://localhost:11434/api/tags

# Pull model manualmente
docker exec $(docker ps -q -f name=sec-llama_ollama) \
  ollama pull codellama:13b

# Info modello
curl http://localhost:11434/api/show \
  -d '{"name":"llama3.1:8b"}'
```

### Backup & Restore

```bash
# Backup database
docker exec $(docker ps -q -f name=sec-llama_postgres) \
  pg_dump -U sec_llama sec_llama | gzip > backup.sql.gz

# Restore database
gunzip < backup.sql.gz | \
  docker exec -i $(docker ps -q -f name=sec-llama_postgres) \
  psql -U sec_llama sec_llama
```

---

## 🌟 Caratteristiche Avanzate

### 1. Installazione con Opzioni

```bash
# Con Nginx reverse proxy
./scripts/install_stack.sh --with-nginx

# Con backup automatico
./scripts/install_stack.sh --with-backup

# Custom stack name
./scripts/install_stack.sh --stack-name production-sec

# Tutto insieme
./scripts/install_stack.sh \
  --stack-name my-security \
  --with-nginx \
  --with-backup
```

### 2. High Availability

```bash
# Cluster multi-nodo
docker swarm init --advertise-addr MANAGER_IP

# Sui worker nodes
docker swarm join --token TOKEN MANAGER_IP:2377

# Deploy su cluster
docker stack deploy -c docker-stack.yml sec-llama
```

### 3. Configurazione Provider Esterni

Oltre a Ollama, puoi configurare:

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Cohere
- Altri provider compatibili

**Nella Web UI**: Vai su AI Configuration → Provider esterni

---

## 📚 Documentazione Completa

- **[DOCKER_STACK_INSTALLATION.md](docs/DOCKER_STACK_INSTALLATION.md)**: Guida installazione completa
- **[WEB_UI_GUIDE.md](docs/WEB_UI_GUIDE.md)**: Guida completa Web UI
- **[MCP_SERVER_GUIDE.md](docs/MCP_SERVER_GUIDE.md)**: Guida MCP Server
- **[FEATURES.md](docs/FEATURES.md)**: Lista completa funzionalità
- **[TRAINING.md](docs/TRAINING.md)**: Guida training IA

---

## 🔒 Sicurezza

### Password Generate

Le password sono generate automaticamente e salvate in `.env`:

```bash
# Visualizza password
cat .env | grep PASSWORD

# Cambia password
nano .env
# Poi ricarica secrets e rideploy stack
```

### HTTPS con Nginx

```bash
# Genera certificato self-signed
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Deploy con Nginx
./scripts/install_stack.sh --with-nginx
```

### API Keys

1. Vai su: http://localhost:8080/api-keys
2. Crea nuova API key
3. Copia la key (mostrata una sola volta!)
4. Usa nelle chiamate API:
   ```bash
   curl -H "X-API-Key: your-key" \
     http://localhost:8765/api/tools
   ```

---

## 🐛 Troubleshooting

### Ollama non si connette

```bash
# Verifica logs
docker service logs sec-llama_ollama

# Verifica API
curl http://localhost:11434/api/tags

# Test da Web UI
# Vai su AI Configuration → Test Connection
```

### Modello non si scarica

```bash
# Verifica spazio disco
df -h

# Pull manuale
docker exec -it $(docker ps -q -f name=sec-llama_ollama) \
  ollama pull llama3.1:8b
```

### Servizio non parte

```bash
# Verifica status
docker service ps sec-llama_web-ui --no-trunc

# Visualizza errori
docker service logs --tail 100 sec-llama_web-ui

# Force restart
docker service update --force sec-llama_web-ui
```

---

## 💡 Prossimi Passi

Dopo l'installazione:

1. ✅ **Configura IA**: http://localhost:8080/ai-config
   - Imposta Ollama host (locale/remoto)
   - Scarica modelli necessari
   - Testa generazione

2. ✅ **Crea API Keys**: http://localhost:8080/api-keys
   - Genera chiavi per accesso programmatico
   - Configura permessi

3. ✅ **Esplora Tools**: http://localhost:8080/tools
   - Prova network discovery
   - Esegui vulnerability scan

4. ✅ **Personalizza**: http://localhost:8080/config
   - Modifica configurazione
   - Adatta alle tue esigenze

---

## 🆘 Supporto

- **Issues**: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)
- **Documentazione**: [docs/](docs/)

---

## 📝 Note Importanti

⚠️ **Prima esecuzione**: Il download del modello LLM può richiedere 5-15 minuti.

⚠️ **Requisiti hardware**: 8GB RAM minimo, 16GB consigliati per prestazioni ottimali.

⚠️ **Rete**: Assicurati che le porte 8080, 8765, 11434 siano disponibili.

✅ **Pronto per produzione**: Usa `--with-nginx` e configura certificati SSL.

✅ **Backup automatici**: Usa `--with-backup` per backup giornalieri automatici.

---

**Made with ❤️ by Sec-Llama Team**

Inizia ora: `./scripts/install_stack.sh` 🚀

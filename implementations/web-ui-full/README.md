# Web UI Full - Interfaccia Web Completa

Interfaccia web completa con configurazione AI, gestione tools, e monitoring.

## 🚀 Quick Start

```bash
# Setup (una volta)
./setup.sh

# Avvia
./start.sh

# Apri browser
open http://localhost:8080
```

## 📦 Installazione

```bash
./setup.sh
```

Questo configura:
- Backend FastAPI
- Frontend Vue.js 3
- Database SQLite
- Ollama (opzionale)

## 🎨 Features

### Dashboard
- Statistiche real-time
- Esecuzioni recenti
- Grafici usage tools
- Stato sistema

### AI Configuration ⭐
- Configura Ollama (locale/remoto)
- Gestisci modelli (pull/delete)
- Test connessione e generazione
- Parametri LLM (temperature, tokens)

### Tools Execution
- Browser tools disponibili
- Form dinamici per parametri
- Esecuzione con risultati real-time
- Export risultati

### Configuration
- Editor YAML con validazione
- Backup e restore
- Download configurazione

### API Keys
- Gestione chiavi API
- Usage tracking
- Permissions

### Audit Logs
- Visualizzatore logs
- Filtri avanzati
- Export JSON/CSV

## ⚙️ Configurazione

### Configurare Ollama Remoto

1. Sul server Ollama:
```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

2. Nella Web UI:
   - Vai su **AI Configuration**
   - Imposta host: `http://SERVER_IP:11434`
   - Test connection
   - Save

### Porte Personalizzate

Modifica `.env`:
```bash
WEB_UI_PORT=9080
```

Poi riavvia:
```bash
./start.sh
```

## 🔧 Development Mode

```bash
./start.sh --dev
```

Questo avvia:
- Backend con auto-reload (port 8080)
- Frontend dev server (port 3000)

## 🏗️ Build per Produzione

```bash
./build.sh
./start.sh --prod
```

## 🐳 Docker (Opzionale)

```bash
docker-compose up -d
```

## 📊 Accesso

- **Web UI**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

## 🔒 Sicurezza

### Cambia Secret Key

Modifica `.env`:
```bash
SECRET_KEY=your-super-secret-key-here
```

### HTTPS (con Nginx)

Vedi `nginx/` directory per configurazione.

## 📚 API Reference

Documentazione API completa:
http://localhost:8080/docs

## 🆘 Troubleshooting

### Frontend non si carica
```bash
cd frontend
npm install
npm run build
```

### Backend errori
```bash
# Check logs
tail -f logs/web_ui.log

# Restart
./start.sh --restart
```

### Ollama non si connette
- Verifica Ollama sia running: `curl http://localhost:11434/api/tags`
- Controlla host in AI Configuration
- Test connection nella Web UI

---

## 🐳 Installazione con Portainer

Per deployare in Portainer:

### Metodo 1: Upload Stack File

1. **Portainer** → **Stacks** → **Add Stack**
2. **Name**: `sec-llama-web-ui`
3. **Upload**: Seleziona `portainer-stack.yml`
4. **Environment variables**: Copia da `portainer-env.txt`
5. **Deploy the stack**

### Metodo 2: Git Repository

1. **Portainer** → **Stacks** → **Add Stack**
2. **Repository URL**: `https://github.com/yourusername/Sec-llama.git`
3. **Compose path**: `implementations/web-ui-full/docker-compose.yml`
4. **Environment variables**: Imposta variabili
5. **Deploy**

### Post-Deploy

```bash
# Pull modello Ollama
docker exec -it <ollama-container-id> ollama pull llama3.1:8b
```

📖 **[Guida Completa Portainer](../../docs/PORTAINER_INSTALL.md)**


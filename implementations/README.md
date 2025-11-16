# 🎯 Sec-Llama - Implementazioni Separate

Ogni implementazione è completamente **indipendente e autosufficiente**.

---

## 📦 Implementazioni Disponibili

Scegli l'implementazione che preferisci:

### 1️⃣ `standalone/` - Uso Locale Semplice
**Per chi vuole**: Usare Sec-Llama come tool da riga di comando locale

```bash
cd implementations/standalone
pip install -r requirements.txt
python main.py scan --network 192.168.1.0/24
```

**Caratteristiche**:
- ✅ Nessun server richiesto
- ✅ Tutto locale
- ✅ Ollama opzionale
- ✅ CLI semplice

---

### 2️⃣ `mcp-stdio/` - MCP Server Locale (Claude Desktop)
**Per chi vuole**: Integrare con Claude Desktop via stdio

```bash
cd implementations/mcp-stdio
./setup.sh
./start.sh
```

**Caratteristiche**:
- ✅ Integrazione Claude Desktop
- ✅ Stdio transport
- ✅ Zero configurazione rete
- ✅ Accesso tools via Claude

**Claude Desktop config**:
```json
{
  "mcpServers": {
    "sec-llama": {
      "command": "/path/to/implementations/mcp-stdio/start.sh"
    }
  }
}
```

---

### 3️⃣ `mcp-http/` - MCP Server Remoto (LAN/Internet)
**Per chi vuole**: Server MCP accessibile da remoto

```bash
cd implementations/mcp-http
./setup.sh
./start.sh --host 0.0.0.0 --port 8765
```

**Caratteristiche**:
- ✅ HTTP/SSE transport
- ✅ API Key authentication
- ✅ Accesso da LAN/Internet
- ✅ Rate limiting
- ✅ Multi-client

---

### 4️⃣ `web-ui-full/` - Interfaccia Web Completa ⭐
**Per chi vuole**: UI grafica completa con configurazione AI

```bash
cd implementations/web-ui-full
./setup.sh
./start.sh
```

Apri: **http://localhost:8080**

**Caratteristiche**:
- ✅ Dashboard real-time
- ✅ Configurazione AI visuale
- ✅ Gestione modelli Ollama
- ✅ Tool execution GUI
- ✅ API Keys management
- ✅ Audit logs viewer

---

### 5️⃣ `docker-dev/` - Docker per Sviluppo
**Per chi vuole**: Ambiente di sviluppo containerizzato

```bash
cd implementations/docker-dev
docker-compose up -d
```

**Caratteristiche**:
- ✅ Hot reload
- ✅ Volume mounts per sviluppo
- ✅ Tutti i servizi in containers
- ✅ Easy debugging

---

### 6️⃣ `docker-production/` - Docker Stack Produzione 🚀
**Per chi vuole**: Deployment production-ready scalabile

```bash
cd implementations/docker-production
./install.sh
```

**Caratteristiche**:
- ✅ Docker Swarm
- ✅ Auto-scaling
- ✅ Health checks
- ✅ Secrets management
- ✅ PostgreSQL + Redis
- ✅ Nginx reverse proxy
- ✅ Automated backups

---

### 7️⃣ `live-usb/` - USB Bootable
**Per chi vuole**: Sistema bootable da USB

```bash
cd implementations/live-usb
sudo ./create-usb.sh /dev/sdX
```

**Caratteristiche**:
- ✅ Bootable USB
- ✅ Persistence storage
- ✅ Pre-configured tools
- ✅ Portable security suite

---

## 🔧 Librerie Condivise

Le implementazioni usano codice condiviso da `shared/`:

```
shared/
├── core/          # Moduli sicurezza (network, code, threat)
├── ai/            # LLM integration e training
└── utils/         # Utility comuni
```

Ogni implementazione importa solo ciò che serve:
```python
from shared.core.network import HostDiscovery
from shared.ai.llm import LLMInterface
```

---

## 🎯 Quale Scegliere?

| Voglio... | Usa |
|-----------|-----|
| Provare velocemente | `standalone/` |
| Integrazione Claude Desktop | `mcp-stdio/` |
| Server accessibile da LAN | `mcp-http/` |
| Interfaccia web grafica | `web-ui-full/` ⭐ |
| Sviluppare/modificare | `docker-dev/` |
| Deploy in produzione | `docker-production/` 🚀 |
| USB bootable | `live-usb/` |

---

## 📚 Documentazione

Ogni implementazione ha la sua documentazione completa:

- `implementations/standalone/README.md`
- `implementations/mcp-stdio/README.md`
- `implementations/mcp-http/README.md`
- `implementations/web-ui-full/README.md`
- `implementations/docker-dev/README.md`
- `implementations/docker-production/README.md`
- `implementations/live-usb/README.md`

---

## 🚀 Quick Start

### Più Semplice (Standalone)
```bash
cd implementations/standalone
pip install -r requirements.txt
python main.py --help
```

### Più Completo (Web UI) ⭐
```bash
cd implementations/web-ui-full
./setup.sh && ./start.sh
# Apri http://localhost:8080
```

### Produzione (Docker Stack) 🚀
```bash
cd implementations/docker-production
./install.sh
# Tutto configurato automaticamente!
```

---

**Nota**: Ogni implementazione è **completamente indipendente**. Scegli quella che preferisci e ignora le altre!

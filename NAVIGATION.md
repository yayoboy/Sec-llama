# 🧭 Navigazione Rapida - Sec-Llama

Guida veloce per trovare quello che ti serve nel progetto riorganizzato.

---

## 🚀 Voglio installare/deployare Sec-Llama

### Installazione Production (Docker Stack) ⭐ CONSIGLIATO
```bash
./scripts/install_stack.sh
```
📁 Vai a: [`deployments/docker-stack/`](deployments/docker-stack/)
📖 Leggi: [DOCKER_STACK_INSTALLATION.md](docs/DOCKER_STACK_INSTALLATION.md)

### Installazione Development (Docker Compose)
```bash
cd deployments/docker
docker-compose up -d
```
📁 Vai a: [`deployments/docker/`](deployments/docker/)

### Creare Live USB Bootable
```bash
cd deployments/live-usb
sudo ./create_persistent_usb.sh /dev/sdX
```
📁 Vai a: [`deployments/live-usb/`](deployments/live-usb/)

---

## 🎨 Voglio usare l'interfaccia Web

### Avviare Web UI
```bash
./scripts/start_web_ui.sh
```
Poi apri: **http://localhost:8080**

📁 Vai a: [`web-ui/`](web_ui/)
📖 Leggi: [WEB_UI_GUIDE.md](docs/WEB_UI_GUIDE.md)

### Configurare l'IA (Ollama remoto/locale)
1. Apri: **http://localhost:8080/ai-config**
2. Configura Ollama host
3. Scarica modelli
4. Testa connessione

---

## 🤖 Voglio configurare l'IA

### Via Web UI ⭐ PIÙ FACILE
http://localhost:8080/ai-config

### Via File di Configurazione
Modifica: [`config/mcp_server_config.yaml`](config/mcp_server_config.yaml)

### Training Custom Models
```bash
cd ai/training
python dataset_manager.py --source nvd
```
📁 Vai a: [`ai/training/`](ai/training/)
📖 Leggi: [TRAINING.md](docs/TRAINING.md)

---

## 🔌 Voglio usare il Server MCP

### Locale (per Claude Desktop)
```bash
python -m mcp-server.server --transport stdio
```

### Remoto (HTTP/SSE)
```bash
python -m mcp-server.server --transport http --port 8765
```

📁 Vai a: [`mcp-server/`](mcp-server/)
📖 Leggi: [MCP_SERVER_GUIDE.md](docs/MCP_SERVER_GUIDE.md)

---

## 💻 Voglio usare i tool di sicurezza

### Network Security
```python
from core.network.discovery import HostDiscovery
from core.network.scanning import PortScanner

discovery = HostDiscovery()
hosts = await discovery.discover_subnet("192.168.1.0/24")

scanner = PortScanner()
results = await scanner.scan(hosts[0], "1-1000")
```
📁 Vai a: [`core/network/`](core/network/)

### Code Analysis
```python
from core.code_analysis import CodeAnalyzer

analyzer = CodeAnalyzer()
vulns = await analyzer.scan_directory("/path/to/code")
```
📁 Vai a: [`core/code_analysis/`](core/code_analysis/)

### Threat Intelligence
```python
from core.threat_intel import ThreatIntel

threat_intel = ThreatIntel()
cve_info = await threat_intel.lookup_cve("CVE-2021-44228")
```
📁 Vai a: [`core/threat_intel/`](core/threat_intel/)

### Tutti i Moduli Core
📁 Vai a: [`core/`](core/)
📖 Leggi: [core/README.md](core/README.md)

---

## 📊 Struttura del Progetto

```
Sec-llama/
│
├── 🚀 deployments/       ← Deployment (Docker, Stack, Live USB)
├── 🛡️ core/             ← Tool di sicurezza
├── 🔌 mcp-server/       ← Server MCP
├── 🎨 web-ui/           ← Interfaccia Web
├── 🤖 ai/               ← IA e Training
├── 💻 cli/              ← CLI
├── 🔧 scripts/          ← Script utility
└── 📚 docs/             ← Documentazione
```

Vedi: [STRUCTURE.md](STRUCTURE.md) per dettagli completi

---

## 📚 Documentazione

| Documento | Descrizione |
|-----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Guida rapida (ITA) |
| [STRUCTURE.md](STRUCTURE.md) | Struttura progetto completa |
| [DOCKER_STACK_INSTALLATION.md](docs/DOCKER_STACK_INSTALLATION.md) | Installazione Docker Stack |
| [WEB_UI_GUIDE.md](docs/WEB_UI_GUIDE.md) | Guida Web UI |
| [MCP_SERVER_GUIDE.md](docs/MCP_SERVER_GUIDE.md) | Guida MCP Server |
| [TRAINING.md](docs/TRAINING.md) | Training modelli IA |
| [FEATURES.md](docs/FEATURES.md) | Lista completa features |

---

## 🎯 Casi d'Uso Comuni

### "Voglio provare Sec-Llama velocemente"
```bash
./scripts/install_stack.sh
# Apri http://localhost:8080
```

### "Voglio configurare Ollama su un server remoto"
1. Sul server remoto:
   ```bash
   export OLLAMA_HOST=0.0.0.0:11434
   ollama serve
   ```
2. In Sec-Llama Web UI: http://localhost:8080/ai-config
3. Imposta host: `http://IP_SERVER:11434`

### "Voglio usare i tool in Python"
```python
from core.network.discovery import HostDiscovery
discovery = HostDiscovery()
hosts = await discovery.discover_subnet("192.168.1.0/24")
```

### "Voglio deployare in produzione"
```bash
./scripts/install_stack.sh --with-nginx --with-backup
```

### "Voglio sviluppare/modificare il codice"
```bash
cd deployments/docker
docker-compose up -d
# Modifica i file nella directory appropriata
```

### "Voglio addestrare un modello custom"
```bash
cd ai/training
python dataset_manager.py --source nvd --limit 10000
python model_trainer.py --base-model llama3.1:8b
```

---

## 🔍 Ricerca Rapida

**Cerco** → **Trovo in**

- Docker Compose → `deployments/docker/`
- Docker Stack → `deployments/docker-stack/`
- Live USB → `deployments/live-usb/`
- Network tools → `core/network/`
- Code analysis → `core/code_analysis/`
- Web security → `core/web_security/`
- MCP Server → `mcp-server/`
- Web UI → `web-ui/`
- IA/LLM → `ai/llm/`
- Training → `ai/training/`
- Prompt templates → `ai/prompts/`
- Script install → `scripts/install_stack.sh`
- Configurazione → `config/`
- Documentazione → `docs/`

---

## 💡 Tips

✅ **Ogni directory ha il suo README** - Leggi `README.md` nella directory per info specifiche

✅ **Import aggiornati** - Usa `from core.` invece di `from modules.`

✅ **Web UI per configurazione** - Usa http://localhost:8080/ai-config per configurare l'IA visivamente

✅ **Un comando per tutto** - `./scripts/install_stack.sh` installa tutto automaticamente

✅ **Scaling facile** - `docker service scale sec-llama_web-ui=3` per scalare

---

## 🆘 Aiuto

**Ho un problema** → Controlla [Troubleshooting](docs/DOCKER_STACK_INSTALLATION.md#troubleshooting)

**Voglio contribuire** → Leggi [STRUCTURE.md](STRUCTURE.md) per capire l'organizzazione

**Ho una domanda** → Apri una [Issue su GitHub](https://github.com/yourusername/Sec-llama/issues)

---

**Inizia ora**: `./scripts/install_stack.sh` 🚀

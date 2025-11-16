# Navigazione Repository Sec-Llama

Questa guida ti aiuta a navigare la nuova struttura del repository, completamente riorganizzata in implementazioni indipendenti.

## 📁 Struttura Repository

```
Sec-llama/
├── README.md                  # Guida principale con confronto implementazioni
├── LICENSE                    # Licenza MIT
├── docs/                      # Documentazione generale
└── implementations/           # 7 implementazioni indipendenti
    ├── standalone/
    ├── mcp-stdio/
    ├── mcp-http/
    ├── web-ui-full/
    ├── docker-dev/
    ├── docker-production/
    └── live-usb/
```

## 🎯 Scegliere l'Implementazione Giusta

### ❓ Quale implementazione usare?

**Vuoi un tool CLI locale rapido?**
→ `implementations/standalone/`

**Vuoi integrare con Claude Desktop?**
→ `implementations/mcp-stdio/`

**Vuoi un server remoto accessibile da rete?**
→ `implementations/mcp-http/`

**Vuoi un'interfaccia web completa?**
→ `implementations/web-ui-full/`

**Stai sviluppando e vuoi un ambiente development?**
→ `implementations/docker-dev/`

**Vuoi deployare in produzione con scaling?**
→ `implementations/docker-production/`

**Vuoi un USB bootable per testing portatile?**
→ `implementations/live-usb/`

## 📦 Struttura Implementazioni

Ogni implementazione è **completamente autocontenuta** con:

### Standalone
```
standalone/
├── README.md              # Documentazione completa
├── setup.sh               # Setup automatico
├── sec-llama.sh           # Script di avvio
├── cli/                   # Codice CLI
├── modules/               # Moduli sicurezza
├── config/                # Configurazioni
├── requirements.txt       # Dipendenze Python
├── database/              # Database locale
├── logs/                  # Log applicazione
└── reports/               # Report generati
```

### MCP stdio
```
mcp-stdio/
├── README.md              # Guida MCP stdio
├── setup.sh               # Setup + config Claude Desktop
├── start.sh               # Avvio server MCP
├── mcp-server/            # Codice server MCP
├── modules/               # Moduli sicurezza
├── config/                # Configurazioni
├── requirements.txt       # Dipendenze base
├── requirements-mcp.txt   # Dipendenze MCP
├── database/
├── logs/
└── reports/
```

### MCP HTTP
```
mcp-http/
├── README.md              # Guida MCP HTTP
├── setup.sh               # Setup + API key generation
├── start.sh               # Avvio server HTTP/SSE
├── mcp-server/            # Server MCP con HTTP
├── modules/               # Moduli sicurezza
├── config/                # Configurazioni
├── requirements.txt       # Dipendenze base
├── requirements-mcp.txt   # Dipendenze MCP
├── .env                   # Variabili ambiente
├── database/
├── logs/
└── reports/
```

### Web UI Full
```
web-ui-full/
├── README.md              # Guida Web UI
├── setup.sh               # Setup backend + frontend
├── start.sh               # Avvio Web UI
├── web/                   # Codice web (se da root)
├── web_ui/                # Codice web UI completa
│   ├── backend/           # FastAPI backend
│   └── frontend/          # Vue.js frontend
├── modules/               # Moduli sicurezza
├── config/                # Configurazioni
├── requirements.txt       # Dipendenze Python
├── static/                # File statici
├── database/
├── logs/
└── reports/
```

### Docker Dev
```
docker-dev/
├── README.md              # Guida Docker development
├── docker-compose.yml     # Stack completo development
├── .env.example           # Variabili ambiente esempio
├── docker/                # Dockerfiles
├── cli/                   # Codice CLI
├── mcp-server/            # Codice MCP server
├── web/                   # Codice web
├── modules/               # Moduli sicurezza
├── config/                # Configurazioni
├── scripts/               # Script utility
├── requirements.txt       # Dipendenze base
└── requirements-mcp.txt   # Dipendenze MCP
```

### Docker Production
```
docker-production/
├── README.md              # Guida deployment produzione
├── install.sh             # Installazione automatica
├── docker-stack/          # Stack Docker Swarm
│   └── docker-stack.yml   # Definizione stack
├── cli/                   # Codice CLI
├── mcp-server/            # Codice MCP server
├── web/                   # Codice web
├── modules/               # Moduli sicurezza
├── config/                # Configurazioni
├── scripts/               # Script di gestione
├── requirements.txt       # Dipendenze base
└── requirements-mcp.txt   # Dipendenze MCP
```

### Live USB
```
live-usb/
├── README.md              # Guida Live USB
├── create-usb.sh          # Creazione USB bootable
├── backup_data.sh         # Backup dati USB
├── setup_persistent_env.sh # Setup ambiente persistente
└── create_persistent_usb.sh # Creazione con persistenza
```

## 🚀 Quick Start per Implementazione

### Standalone
```bash
cd implementations/standalone
./setup.sh
./sec-llama.sh scan network 192.168.1.0/24
```

### MCP stdio
```bash
cd implementations/mcp-stdio
./setup.sh
# Riavvia Claude Desktop
```

### MCP HTTP
```bash
cd implementations/mcp-http
./setup.sh
source .env
./start.sh
```

### Web UI Full
```bash
cd implementations/web-ui-full
./setup.sh
./start.sh
# Apri http://localhost:8080
```

### Docker Dev
```bash
cd implementations/docker-dev
cp .env.example .env
docker-compose up -d
# Accedi http://localhost:8080
```

### Docker Production
```bash
cd implementations/docker-production
./install.sh
# Stack deployato automaticamente
```

### Live USB
```bash
cd implementations/live-usb
sudo ./create-usb.sh /dev/sdX
# Boot da USB
```

## 📖 Documentazione

### README Principale
- `README.md` - Panoramica, confronto implementazioni, getting started

### README Implementazioni
Ogni implementazione ha il suo README dettagliato:
- `implementations/standalone/README.md` - CLI usage
- `implementations/mcp-stdio/README.md` - Claude Desktop integration
- `implementations/mcp-http/README.md` - Remote server setup
- `implementations/web-ui-full/README.md` - Web interface guide
- `implementations/docker-dev/README.md` - Development environment
- `implementations/docker-production/README.md` - Production deployment
- `implementations/live-usb/README.md` - Bootable USB creation

### Docs Generali
- `docs/` - Documentazione cross-implementation

## 🔧 File Comuni

### In ogni implementazione Python-based:

**requirements.txt** - Dipendenze Python base:
- Moduli sicurezza (scapy, python-nmap, ecc.)
- LLM integration (ollama-python, langchain)
- Utility comuni

**requirements-mcp.txt** - Dipendenze MCP (solo mcp-*):
- MCP SDK
- FastAPI (per HTTP)
- Server dependencies

**config/** - Configurazioni:
- `config.example.yaml` - Configurazione esempio
- `mcp_server_config.yaml` - Config MCP server

**modules/** - Moduli sicurezza:
- `network/` - Network security
- `code_review/` - Code analysis
- `threat_intel/` - Threat intelligence
- `incident_response/` - IR automation
- `reporting/` - Report generation
- E altri...

## 🎯 Come Contribuire

### Modificare una singola implementazione:
```bash
cd implementations/[nome-implementazione]
# Modifica file
# Test localmente
git add .
git commit -m "feat(nome-implementazione): descrizione"
git push
```

### Modificare codice condiviso tra implementazioni:
**Non c'è più codice condiviso!** Ogni implementazione è indipendente. Se vuoi una modifica in più implementazioni:

1. Applica la modifica in ogni implementazione
2. O crea script per sincronizzare

### Aggiungere nuova implementazione:
```bash
mkdir implementations/nuova-implementazione
# Copia moduli necessari
# Crea README.md, setup.sh
# Aggiungi a README.md principale
```

## ❓ FAQ

**Q: Posso usare più implementazioni insieme?**
A: Sì! Sono completamente indipendenti. Puoi avere standalone per test locali + docker-production per produzione.

**Q: Come aggiorno Sec-Llama?**
A: `git pull origin main` poi ri-esegui `./setup.sh` nell'implementazione usata.

**Q: Dove vanno i report?**
A: Ogni implementazione ha la sua cartella `reports/`

**Q: I database sono condivisi?**
A: No, ogni implementazione ha il suo database in `database/`

**Q: Posso spostare un'implementazione su altro PC?**
A: Sì! Copia l'intera cartella implementazione. È autocontenuta.

**Q: Come configuro Ollama remoto?**
A: Modifica `config/config.example.yaml` in ogni implementazione, oppure usa Web UI per configurazione visuale.

**Q: Devo installare tutto?**
A: No! Scegli solo l'implementazione che ti serve. Ogni implementazione installa solo le sue dipendenze.

## 📞 Supporto

- **Issues**: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)
- **Docs**: `docs/` in questo repository

---

**Versione struttura**: 2.0 - Implementazioni completamente indipendenti
**Ultimo aggiornamento**: 2025-11-16

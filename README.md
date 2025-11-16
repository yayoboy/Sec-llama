# 🛡️ Sec-Llama - Local LLM Security Suite

**Complete cybersecurity testing platform powered by local LLMs for LAN deployment**

Una suite completa per security testing, vulnerability assessment, e AI-powered security analysis. **100% locale e privato.**

---

## 🎯 Overview

Sec-Llama è una piattaforma unificata di cybersecurity testing che combina:

- ✅ **LLM Remoto**: Ollama o LM Studio su PC dedicato
- ✅ **Docker Deployment**: Container orchestration con Docker Compose o Portainer
- ✅ **Web UI Completa**: Gestione e configurazione via interfaccia web
- ✅ **LAN Optimized**: Progettato per deployment su rete locale
- ✅ **Production Ready**: PostgreSQL, Redis, health checks

---

## 🚀 Quick Start (3 Comandi!)

### Deploy Completo in 3 Step

```bash
# 1. Configura environment
cp .env.example .env
nano .env  # Modifica OLLAMA_HOST, passwords, SECRET_KEY

# 2. Avvia tutto
docker-compose up -d

# 3. Accedi alla Web UI
# Browser: http://localhost:8080
# Login: admin / (password dal .env)
```

**✨ FATTO!** Hai ora:
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Web UI completa su porta 8080
- ✅ Connessione al tuo LLM remoto

### 📚 Guide Dettagliate

- **⚡ Deploy Rapido**: [QUICK_START.md](QUICK_START.md) - Setup completo in 5 minuti
- **🐳 Deploy Portainer**: [PORTAINER_DEPLOY.md](PORTAINER_DEPLOY.md) - Deploy con Portainer (GUI) in 3 click
- **🔧 Deploy Avanzato**: [DEPLOYMENT.md](DEPLOYMENT.md) - Configurazione production completa
- **📖 Features Complete**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Tutte le funzionalità disponibili

---

## 🏗️ Architettura

```
┌─────────────────────────────────────────────────────────┐
│                    LAN Network                          │
│                                                         │
│  ┌──────────────┐     ┌──────────────┐                │
│  │ LLM Server   │     │ Sec-Llama    │                │
│  │              │     │ Server       │                │
│  │ • Ollama     │────▶│ • Web UI     │                │
│  │   OR         │     │ • PostgreSQL │                │
│  │ • LM Studio  │     │ • Redis      │                │
│  │              │     │ • Modules    │                │
│  └──────────────┘     └──────────────┘                │
│  192.168.1.100        192.168.1.10                     │
│  :11434 / :1234       :8080                            │
│                                                         │
│  ┌──────────────────────────────────┐                 │
│  │   Client Browsers                │                 │
│  │   http://192.168.1.10:8080       │                 │
│  └──────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

**Componenti**:
- **LLM Server**: PC dedicato con Ollama o LM Studio
- **Sec-Llama Server**: Container Docker (Web UI + Database + Cache)
- **Clients**: Accesso via browser alla porta 8080

---

## 🎯 Core Security Features

### 🌐 Network Security
- Network discovery (ARP/ICMP/TCP)
- Smart port scanning (Nmap integration)
- Service analysis + CVE lookup
- Wireless security (WiFi/Bluetooth)
- Traffic analysis (PCAP parsing)
- Attack planning

### 💻 Application Security
- SAST (Python, JS, Java, Go, PHP)
- Code review assistant
- Dependency scanning
- Container security
- API fuzzing (REST/GraphQL)

### 🎯 Penetration Testing
- Exploit suggestions
- Payload crafting
- Attack surface analysis
- Post-exploitation strategies

### 🔧 Tool Integrations
- Metasploit
- Burp Suite
- BloodHound
- Trivy
- Nmap/Masscan

### 🔍 Threat Intelligence
- CVE lookup (NVD API)
- IOC analysis
- OSINT gathering

### 📝 Log Analysis & SIEM
- Multi-format parsing
- Attack detection
- Anomaly detection
- Real-time monitoring

### 🚨 Incident Response
- IR automation
- NIST playbooks
- Containment planning
- IOC tracking

### 📊 Advanced Reporting
- Executive reports
- Technical reports
- Compliance reports (OWASP, PCI-DSS, ISO 27001)
- PDF/HTML export

### 🎓 LLM Training & Fine-Tuning
- Dataset collection (CVE/exploit data)
- Model training (Ollama, LoRA/QLoRA)
- Model evaluation
- Custom datasets

---

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](implementations/lan-server/QUICK_START.md)** - Start in 5 minutes
- **[Complete Documentation](implementations/lan-server/README.md)** - Full implementation guide
- **[Configuration Guide](implementations/lan-server/.env.example)** - Environment variables

### Deployment Options
- **Docker Compose**: Development and production
- **Portainer**: Stack deployment with UI
- **Manual Setup**: Local development without Docker

---

## 🔧 Configuration

### LLM Configuration

**Supporta due provider**:

1. **Ollama** (Native API)
   - Host: `http://192.168.1.100:11434`
   - Models: llama3.1:8b, llama3.1:70b, mistral, codellama

2. **LM Studio** (OpenAI-compatible API)
   - Host: `http://192.168.1.100:1234`
   - Qualsiasi modello compatibile

**Configurazione via**:
- File `.env` per Docker
- Web UI → AI Configuration
- File YAML (opzionale)

### Database & Caching

- **PostgreSQL 15**: Database principale
- **Redis 7**: Caching e session storage
- **Backup automatici**: Configurabili
- **Persistenza**: Volumes Docker

---

## 📊 Example Commands

Dalla Web UI puoi eseguire:

### Network Security
```bash
# Host Discovery
POST /api/tools/network/discover
{ "network": "192.168.1.0/24" }

# Port Scanning with AI
POST /api/tools/network/scan
{ "host": "192.168.1.10", "ai_analysis": true }
```

### Threat Intelligence
```bash
# CVE Lookup
POST /api/tools/threat/cve
{ "cve_id": "CVE-2024-1234" }

# IOC Analysis
POST /api/tools/threat/ioc
{ "ioc": "192.168.1.100", "type": "ip" }
```

### Code Security
```bash
# SAST Scan
POST /api/tools/code/scan
{ "path": "./myapp", "language": "python" }

# Container Scan
POST /api/tools/container/scan
{ "image": "nginx:latest" }
```

---

## 🐳 Docker Management

### Basic Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart

# Update images
docker-compose pull
docker-compose up -d
```

### Portainer Deployment

1. Access Portainer UI: `http://your-portainer:9000`
2. Go to: **Stacks** → **Add Stack**
3. Name: `sec-llama`
4. Upload: `implementations/lan-server/portainer-stack.yml`
5. Add environment variables from: `portainer-env.txt`
6. **Deploy**

---

## 🏗️ Project Structure

```
Sec-llama/
├── implementations/
│   └── lan-server/              # Unified implementation
│       ├── docker-compose.yml   # Docker Compose config
│       ├── Dockerfile           # Web UI container
│       ├── .env.example         # Environment template
│       ├── portainer-stack.yml  # Portainer stack
│       ├── requirements.txt     # Python dependencies
│       ├── setup.sh             # Setup script
│       ├── README.md            # Full documentation
│       ├── QUICK_START.md       # Quick start guide
│       │
│       ├── core/                # Core modules
│       │   ├── config.py        # Configuration
│       │   ├── llm_interface.py # LLM integration
│       │   └── prompt_templates.py
│       │
│       ├── modules/             # Security modules
│       │   ├── network/
│       │   ├── threat_intel/
│       │   ├── code_review/
│       │   ├── vuln_scanner/
│       │   ├── container_security/
│       │   ├── api_security/
│       │   ├── log_analyzer/
│       │   ├── incident_response/
│       │   ├── pentest_assistant/
│       │   ├── training/
│       │   └── reporting/
│       │
│       ├── web_ui/              # Web interface
│       │   ├── backend/         # FastAPI
│       │   └── frontend/        # Vue.js
│       │
│       └── config/              # Config files
│
├── docs/                        # Documentation
├── examples/                    # Examples (optional)
└── README.md                    # This file
```

---

## 🔒 Security Best Practices

### Before Production

- [ ] Cambia **tutte** le password di default in `.env`
- [ ] Genera `SECRET_KEY` e `JWT_SECRET_KEY` sicuri (32+ caratteri)
- [ ] Configura firewall per limitare accesso
- [ ] Configura HTTPS con reverse proxy (Nginx/Traefik)
- [ ] Imposta `ALLOWED_ORIGINS` a domini specifici (non `*`)
- [ ] Abilita rate limiting
- [ ] Configura backup automatici database
- [ ] Rivedi permessi moduli di sicurezza

### Firewall Rules

```bash
# Sul server LLM (Ollama)
sudo ufw allow 11434/tcp

# Sul server LLM (LM Studio)
sudo ufw allow 1234/tcp

# Sul server Sec-Llama
sudo ufw allow 8080/tcp  # Web UI
sudo ufw allow 5432/tcp  # PostgreSQL (solo se accesso esterno necessario)
sudo ufw allow 6379/tcp  # Redis (solo se accesso esterno necessario)
```

---

## 🐛 Troubleshooting

### Cannot connect to LLM server

```bash
# Test connettività
ping 192.168.1.100

# Test API Ollama
curl http://192.168.1.100:11434/api/tags

# Test API LM Studio
curl http://192.168.1.100:1234/v1/models

# Verifica firewall
sudo ufw status
```

### Web UI not accessible

```bash
# Verifica container
docker-compose ps

# Verifica logs
docker-compose logs web-ui

# Verifica porta
netstat -tlnp | grep 8080
```

### Database errors

```bash
# Logs PostgreSQL
docker-compose logs postgres

# Test connessione
docker exec -it sec-llama-postgres psql -U sec_llama -d sec_llama
```

---

## 📊 Performance

### Resource Requirements

**Minimo**:
- CPU: 2 cores
- RAM: 4 GB
- Disk: 20 GB
- Network: 100 Mbps

**Raccomandato**:
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 50+ GB SSD
- Network: 1 Gbps

**LLM Server** (separato):
- Dipende dal modello
- llama3.1:8b → 8 GB RAM
- llama3.1:70b → 64 GB RAM

---

## ⚖️ Legal & Ethics

**IMPORTANTE:** Questo tool è destinato SOLO a:
- ✅ Security testing autorizzato
- ✅ Competizioni CTF
- ✅ Ricerca sulla sicurezza
- ✅ Ambienti personali di test/lab
- ✅ Scopi educativi

**NON usare per:**
- ❌ Accesso non autorizzato a sistemi
- ❌ Attività illegali
- ❌ Testing senza permesso esplicito

Gli utenti sono responsabili dell'uso appropriato di questo software.

---

## 🤝 Contributing

Contributi benvenuti!

1. Fork del repository
2. Crea feature branch
3. Commit delle modifiche
4. Push al branch
5. Apri Pull Request

---

## 📄 License

MIT License - vedi file LICENSE

---

## 🙏 Credits

- **Ollama**: Local LLM runtime
- **LM Studio**: Local LLM interface
- **FastAPI**: Modern web framework
- **Vue.js**: Progressive JavaScript framework
- **PostgreSQL**: Reliable database
- **Redis**: Fast caching
- **Docker**: Containerization
- **Nmap**: Network scanning
- Community open source security tools

---

## 📞 Support

- **Documentation**: Vedi cartella `implementations/lan-server/`
- **Issues**: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
- **Quick Start**: [QUICK_START.md](implementations/lan-server/QUICK_START.md)

---

## 🚀 Next Steps

1. **Deploy**: Segui la [Quick Start Guide](implementations/lan-server/QUICK_START.md)
2. **Configure**: Imposta il tuo LLM server remoto
3. **Explore**: Prova i vari moduli di sicurezza
4. **Secure**: Applica le security best practices
5. **Scale**: Configura backup e monitoring

---

Made with ❤️ for the cybersecurity community

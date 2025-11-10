# 🛡️ Sec-Llama Suite

**Local LLM-Powered Cybersecurity Testing Suite**

Una suite completa per security testing e vulnerability assessment che utilizza Large Language Models locali (Ollama) per analisi intelligenti e automatizzazione avanzata.

## 🎯 Caratteristiche Principali

### 🌐 Network Security Testing
- **Network Discovery**: Host discovery intelligente con fingerprinting OS
- **Smart Port Scanning**: Scan ottimizzati con suggerimenti AI
- **Service Analysis**: Detection + CVE lookup automatico
- **Wireless Security**: WiFi/Bluetooth/IoT testing
- **Traffic Analysis**: PCAP parsing e anomaly detection
- **Attack Planning**: Chain generation con LLM reasoning
- **MITM Testing**: ARP poisoning, SSL stripping, DNS spoofing
- **Continuous Monitoring**: Real-time threat detection

### 💻 Application Security
- **SAST**: Static code analysis per vulnerabilità
- **Code Review**: Security-focused code review automatico
- **Dependency Check**: CVE scanning per librerie
- **Container Security**: Docker/Kubernetes scanning

### 🎯 Penetration Testing
- **Exploit Suggestions**: CVE matching e exploit generation
- **Payload Crafting**: Custom payload con evasion techniques
- **Post-Exploitation**: Lateral movement e privilege escalation
- **Report Generation**: Report professionali automatici

### 🔍 Threat Intelligence
- **IOC Analysis**: Indicators of Compromise
- **CVE Research**: Database CVE locale con RAG
- **OSINT**: Open Source Intelligence gathering
- **Malware Analysis**: Static analysis assistita

### 📊 Log Analysis & SIEM
- **Log Parsing**: Multi-format log analysis
- **Anomaly Detection**: Pattern recognition
- **Correlation**: Event correlation intelligente
- **Alerting**: Smart alerts via LLM

## 🏗️ Architettura

```
sec-llama-suite/
├── core/                   # Core functionality
│   ├── llm_interface.py   # Ollama/LLM abstraction
│   ├── prompt_templates.py # Security prompts
│   └── config.py          # Configuration
├── modules/               # Security modules
│   ├── network/          # Network security
│   ├── vuln_scanner/     # Vulnerability scanning
│   ├── pentest_assistant/# Pentest automation
│   ├── threat_intel/     # Threat intelligence
│   └── ...
├── integrations/         # Tool integrations
│   ├── nmap_integration.py
│   ├── metasploit_integration.py
│   └── ...
├── agents/              # Multi-agent system
├── cli/                 # CLI interface
└── web/                 # Web dashboard
```

## 🚀 Quick Start

### Prerequisiti
```bash
# Installa Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Scarica un modello (es. Llama 3.1)
ollama pull llama3.1:8b
# Per analisi più complesse:
ollama pull llama3.1:70b
```

### Installazione
```bash
# Clone repository
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Installa dipendenze
pip install -r requirements.txt

# O usa Docker
docker-compose up -d
```

### Configurazione
```bash
# Copia configurazione di esempio
cp config/config.example.yaml config/config.yaml

# Modifica con il tuo editor
nano config/config.yaml
```

## 📚 Esempi di Utilizzo

### Network Security

```bash
# Network discovery
sec-llama network discover --subnet 192.168.1.0/24

# Smart port scanning con AI
sec-llama network scan --host 192.168.1.10 --ai-suggest

# Vulnerability assessment completo
sec-llama network vuln-scan --network 192.168.1.0/24 --depth full

# Traffic analysis
sec-llama traffic analyze --pcap capture.pcap --find-credentials

# Wireless audit
sec-llama wireless scan --interface wlan0
sec-llama wireless audit --ssid "MyNetwork"

# Attack planning
sec-llama attack-plan --target 192.168.1.0/24 --objective "domain-admin"

# Continuous monitoring
sec-llama monitor start --network 192.168.1.0/24
```

### Code Security

```bash
# Scan vulnerabilità nel codice
sec-llama code scan --path ./myapp --language python

# Code review di una PR
sec-llama code review --pr 123 --repo myorg/myrepo

# Dependency check
sec-llama code deps --path ./myapp --check-cve
```

### Threat Intelligence

```bash
# Analisi IOC
sec-llama threat-intel ioc --indicator 192.168.1.100

# CVE lookup
sec-llama threat-intel cve --id CVE-2024-1234

# OSINT
sec-llama threat-intel osint --target example.com
```

### Penetration Testing

```bash
# Exploit suggestions
sec-llama pentest exploit --service "Apache 2.4.49"

# Payload generation
sec-llama pentest payload --type reverse-shell --target windows

# Report generation
sec-llama pentest report --scan-results results.json --format pdf
```

### Natural Language Queries

```bash
# Interroga il sistema in linguaggio naturale
sec-llama ask "Quali host hanno RDP esposto con autenticazione debole?"
sec-llama ask "Mostrami vulnerabilità critiche nella rete"
sec-llama ask "Genera un piano di attacco per il target 192.168.1.10"
```

## 🔧 Configurazione

### config.yaml

```yaml
llm:
  provider: "ollama"
  model: "llama3.1:8b"
  base_url: "http://localhost:11434"
  temperature: 0.7

network:
  default_timeout: 30
  max_threads: 10
  stealth_mode: false

scanning:
  nmap_path: "/usr/bin/nmap"
  masscan_path: "/usr/bin/masscan"

reporting:
  output_dir: "./reports"
  format: "pdf"

database:
  cve_db_path: "./database/cve.db"
  network_inventory: "./database/network.db"
```

## 🐳 Docker Deployment

```bash
# Build
docker build -t sec-llama-suite .

# Run
docker run -it --rm \
  --network host \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/reports:/app/reports \
  sec-llama-suite

# O usa docker-compose
docker-compose up -d
```

## 🛠️ Integrazioni

### Tools Supportati
- **Nmap**: Port scanning e service detection
- **Masscan**: Fast scanning
- **Metasploit**: Exploitation framework
- **Wireshark/tshark**: Traffic analysis
- **Aircrack-ng**: Wireless security
- **Bettercap**: Network attacks
- **Nuclei**: Template-based scanning
- **BloodHound**: AD analysis
- **Burp Suite**: Web application testing

## 📖 Documentazione

- [Guida Completa](docs/guide.md)
- [API Reference](docs/api.md)
- [Esempi Avanzati](docs/examples.md)
- [Contribuire](docs/contributing.md)

## ⚖️ Legal & Etica

**IMPORTANTE**: Questo tool è destinato SOLO a:
- ✅ Test di sicurezza autorizzati
- ✅ CTF e competizioni di sicurezza
- ✅ Ricerca sulla sicurezza
- ✅ Ambienti di test/lab personali
- ✅ Scopi educativi

**NON utilizzare per:**
- ❌ Accesso non autorizzato a sistemi
- ❌ Attività illegali
- ❌ Test senza permesso esplicito

L'utente è responsabile dell'uso appropriato di questo software.

## 🤝 Contribuire

Contributi benvenuti! Vedi [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE)

## 🙏 Credits

- **Ollama**: Local LLM runtime
- **LangChain**: LLM framework
- **Nmap**: Network scanning
- Community open source security tools

## 📞 Supporto

- Issues: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)

---

Made with ❤️ for the cybersecurity community

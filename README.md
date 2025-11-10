# 🛡️ Sec-Llama Suite

**The Most Comprehensive Local LLM-Powered Cybersecurity Testing Platform**

Una suite **enterprise-grade** completa per security testing, vulnerability assessment, e training di modelli LLM specializzati in sicurezza informatica. **100% locale e privato.**

---

## ⚡ Quick Stats

- 🎯 **90+ Security Features**
- 🤖 **4 Specialized AI Agents**
- 🔧 **10+ Tool Integrations**
- 📊 **3 Report Formats**
- 🎓 **Complete Training System**
- 💯 **100% Local & Private**

---

## 🎯 Core Features

### 🌐 **Network Security Testing**
- ✅ **Network Discovery**: ARP/ICMP/TCP scanning con fingerprinting OS
- ✅ **Smart Port Scanning**: Nmap integration con AI-suggested strategies
- ✅ **Service Analysis**: Version detection + CVE lookup automatico
- ✅ **Wireless Security**: WiFi/Bluetooth/IoT auditing
- ✅ **Traffic Analysis**: PCAP parsing, anomaly detection, credential extraction
- ✅ **Attack Planning**: AI-powered attack chain generation
- ✅ **MITM Testing**: ARP poisoning, SSL stripping, DNS spoofing
- ✅ **Continuous Monitoring**: Real-time threat detection

### 💻 **Application Security**
- ✅ **SAST**: Multi-language static code analysis (Python, JS, Java, Go, PHP)
- ✅ **Code Review Assistant**: Git/GitHub integration per review automatico
- ✅ **Dependency Check**: CVE scanning per librerie
- ✅ **Container Security**: Docker image + runtime scanning
- ✅ **API Security**: REST/GraphQL fuzzing e testing

### 🎯 **Penetration Testing**
- ✅ **Exploit Suggestions**: CVE matching e exploit generation
- ✅ **Payload Crafting**: Custom payload con evasion techniques
- ✅ **Attack Surface Analysis**: Risk assessment e prioritization
- ✅ **Post-Exploitation**: Lateral movement strategies

### 🔧 **Security Tool Integrations** 🆕
- ✅ **Metasploit**: Automated exploitation e payload generation
- ✅ **Burp Suite**: Web app scanning e vulnerability detection
- ✅ **BloodHound**: Active Directory attack path analysis
- ✅ **Trivy**: Container vulnerability scanning
- ✅ **Nmap/Masscan**: Network scanning automation

### 🤖 **Multi-Agent System** 🆕
- ✅ **Recon Agent**: Network discovery specialist
- ✅ **Exploit Agent**: Vulnerability exploitation expert
- ✅ **Defense Agent**: Blue team defensive specialist
- ✅ **Coordinator**: Orchestrates collaborative assessments
- ✅ Inter-agent communication e knowledge sharing

### 🔍 **Threat Intelligence**
- ✅ **CVE Lookup**: NVD API integration con AI analysis
- ✅ **IOC Analysis**: Auto-type detection e threat classification
- ✅ **OSINT**: Open Source Intelligence gathering

### 📝 **Log Analysis & SIEM** 🆕
- ✅ **Multi-format Parsing**: Apache, Nginx, Auth logs
- ✅ **Attack Detection**: SQL injection, XSS, LFI, RFI patterns
- ✅ **Anomaly Detection**: AI-powered statistical analysis
- ✅ **Real-time Monitoring**: Continuous log analysis

### 🚨 **Incident Response** 🆕
- ✅ **IR Automation**: Incident tracking e management
- ✅ **NIST Playbooks**: Automated response plan generation
- ✅ **Containment Planning**: AI-generated containment actions
- ✅ **IOC Tracking**: Indicator management

### 📊 **Advanced Reporting** 🆕
- ✅ **Executive Reports**: Business-focused summaries
- ✅ **Technical Reports**: Detailed findings
- ✅ **Compliance Reports**: OWASP, PCI-DSS, ISO 27001
- ✅ **PDF/HTML Export**: Professional report generation

### 🎓 **LLM Training & Fine-Tuning** 🆕
- ✅ **Dataset Collection**: Automated CVE/exploit data collection
- ✅ **Model Training**: Ollama, LoRA/QLoRA, Unsloth integration
- ✅ **Model Evaluation**: Security-specific benchmarks
- ✅ **Custom Datasets**: Create proprietary security models
- ✅ **Progressive Training**: Continuous model improvement

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

## 📚 Quick Start Examples

### 🌐 Network Security

```bash
# Discover hosts
sec-llama network discover --subnet 192.168.1.0/24

# Smart AI-powered port scanning
sec-llama network scan --host 192.168.1.10 --ai-suggest

# Full vulnerability assessment
sec-llama network vuln-scan --network 192.168.1.0/24 --depth full

# Analyze network traffic
sec-llama traffic analyze --pcap capture.pcap
sec-llama traffic find-creds --pcap capture.pcap

# WiFi security audit
sec-llama wireless scan --interface wlan0
```

### 💻 Application Security

```bash
# SAST code scanning
sec-llama code scan --path ./myapp --language python

# Git commit review
sec-llama review commit --hash abc123

# GitHub PR review
sec-llama review pr --number 42 --repo owner/repo

# Container security
sec-llama container scan-image --image nginx:latest

# API fuzzing
sec-llama api fuzz --url https://api.example.com --endpoint /users
```

### 🤖 Multi-Agent Collaboration

```bash
# Run collaborative security assessment
sec-llama agent collab-assess --target 192.168.1.0/24

# Check agent status
sec-llama agent status
```

### 📝 Log Analysis & SIEM

```bash
# Analyze logs for attacks
sec-llama logs analyze --file /var/log/apache2/access.log

# Find attack patterns
sec-llama logs find-attacks --file /var/log/auth.log
```

### 🚨 Incident Response

```bash
# Create incident
sec-llama incident create \
  --title "Ransomware Attack" \
  --severity CRITICAL

# Execute containment
sec-llama incident contain --id INC-0001
```

### 🎓 LLM Training

```bash
# Collect CVE training data
sec-llama train collect-dataset --type cve --max-items 10000

# Prepare training dataset
sec-llama train prepare-data \
  --datasets "cve_dataset.json,security_qa.json" \
  --format alpaca

# Fine-tune model
sec-llama train fine-tune \
  --base-model llama3.1:8b \
  --dataset training_data.json \
  --name sec-llama-8b

# Evaluate model
sec-llama train evaluate --model sec-llama-8b

# Compare models
sec-llama train compare --models "llama3.1:8b,sec-llama-8b"
```

### 🔍 Threat Intelligence

```bash
# CVE lookup
sec-llama threat cve --id CVE-2024-1234

# Search CVEs
sec-llama threat cve-search --keyword "apache"

# IOC analysis
sec-llama threat ioc --indicator 192.168.1.100
```

### 🎯 Penetration Testing

```bash
# Generate attack plan
sec-llama pentest attack-plan --target 192.168.1.10 --objective "gain access"

# Find exploits
sec-llama pentest exploit --service "Apache" --version "2.4.49"

# Generate payload
sec-llama pentest payload --type reverse_shell --os linux
```

### 📊 Reporting

```bash
# Generate executive report
sec-llama report generate --target "Corporate Network" --type executive --format pdf

# Generate technical report
sec-llama report generate --target "Web Server" --type technical --format html
```

### 💬 Natural Language Queries

```bash
# Ask questions in plain English
sec-llama ask "How do I test for SQL injection?"
sec-llama ask "What are the steps for privilege escalation on Linux?"
sec-llama ask "Generate an attack plan for this network"
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

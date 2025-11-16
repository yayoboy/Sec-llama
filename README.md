# 🛡️ Sec-Llama - Local LLM Security Suite

**Complete cybersecurity testing platform powered by local LLMs with multiple deployment options**

Una suite completa per security testing, vulnerability assessment, e AI-powered security analysis. **100% locale e privato.**

---

## 🎯 Choose Your Implementation

Sec-Llama offre **7 implementazioni indipendenti** per diversi use case. Scegli quella più adatta alle tue esigenze:

| Implementation | Best For | Setup Time | Requirements |
|---------------|----------|------------|--------------|
| **[Standalone](#-standalone)** | Quick local use, CLI tools | 2 min | Python 3.8+ |
| **[MCP stdio](#-mcp-stdio)** | Claude Desktop integration | 5 min | Python 3.8+, Claude Desktop |
| **[MCP HTTP](#-mcp-http)** | Remote access, LAN deployment | 5 min | Python 3.8+ |
| **[Web UI Full](#-web-ui-full)** | Complete web interface + AI config | 10 min | Python 3.8+, Node.js |
| **[Docker Dev](#-docker-dev)** | Development environment | 5 min | Docker |
| **[Docker Production](#-docker-production)** | Production deployment, scaling | 15 min | Docker Swarm |
| **[Live USB](#-live-usb)** | Portable, boot from USB | 20 min | USB 32GB+ |

---

## 🚀 Quick Start by Implementation

### 📦 Standalone

**Perfect for:** Quick local use, command-line security testing

```bash
cd implementations/standalone
./setup.sh
./sec-llama.sh scan network 192.168.1.0/24
./sec-llama.sh threat cve CVE-2024-1234
```

**Features:**
- ✅ CLI tool for immediate use
- ✅ All security modules
- ✅ Local Ollama integration
- ✅ Report generation

📚 **[Standalone Guide](implementations/standalone/README.md)**

---

### 🔌 MCP stdio

**Perfect for:** Using Sec-Llama tools inside Claude Desktop

```bash
cd implementations/mcp-stdio
./setup.sh
./start.sh
# Restart Claude Desktop - tools will appear automatically
```

**Features:**
- ✅ 8+ security tools in Claude Desktop
- ✅ stdio transport (local only)
- ✅ Zero configuration
- ✅ Automatic tool discovery

📚 **[MCP stdio Guide](implementations/mcp-stdio/README.md)**

---

### 🌐 MCP HTTP

**Perfect for:** Remote access, team collaboration, LAN deployment

```bash
cd implementations/mcp-http
./setup.sh
./start.sh
# Access from: http://localhost:8765
```

**Features:**
- ✅ HTTP/SSE transport
- ✅ API key authentication
- ✅ Rate limiting
- ✅ Multi-client support
- ✅ Audit logging

📚 **[MCP HTTP Guide](implementations/mcp-http/README.md)**

---

### 🎨 Web UI Full

**Perfect for:** Complete web interface with AI configuration

```bash
cd implementations/web-ui-full
./setup.sh
./start.sh
# Open: http://localhost:8080
```

**Features:**
- ✅ **AI Configuration UI** - Configure local/remote Ollama
- ✅ **Model Management** - Pull, delete, test models
- ✅ **Dashboard** - Real-time statistics
- ✅ **Tools Execution** - Web-based security tools
- ✅ **API Keys Management** - Generate and manage keys
- ✅ **Audit Logs** - Complete activity tracking
- ✅ **Report Export** - PDF/HTML/JSON

📚 **[Web UI Full Guide](implementations/web-ui-full/README.md)**

---

### 🐳 Docker Dev

**Perfect for:** Development environment with all services

```bash
cd implementations/docker-dev
docker-compose up -d
# Access: http://localhost:8080
```

**Features:**
- ✅ Complete dev environment
- ✅ Hot reload
- ✅ PostgreSQL + Redis
- ✅ Ollama container
- ✅ Easy debugging

📚 **[Docker Dev Guide](implementations/docker-dev/README.md)**

---

### 🏭 Docker Production

**Perfect for:** Production deployment, high availability, scaling

```bash
cd implementations/docker-production
./install.sh
# Stack deployed with auto-scaling
```

**Features:**
- ✅ **Docker Stack** - Swarm orchestration
- ✅ **Auto-scaling** - Scale services on demand
- ✅ **Secrets Management** - Secure credentials
- ✅ **Health Checks** - Automatic recovery
- ✅ **Nginx Reverse Proxy** - HTTPS, rate limiting
- ✅ **Automatic Backups** - Scheduled database backups
- ✅ **High Availability** - Multi-node support

📚 **[Docker Production Guide](implementations/docker-production/README.md)**

---

### 💿 Live USB

**Perfect for:** Portable security testing, boot from USB

```bash
cd implementations/live-usb
sudo ./create-usb.sh /dev/sdX
# Boot from USB and run Sec-Llama
```

**Features:**
- ✅ Bootable USB with persistence
- ✅ Pre-configured Kali/Parrot
- ✅ All tools pre-installed
- ✅ Portable LLM models
- ✅ External storage support

📚 **[Live USB Guide](implementations/live-usb/README.md)**

---

## 🎯 Core Security Features

All implementations include these core capabilities:

### 🌐 Network Security
- Network discovery (ARP/ICMP/TCP)
- Smart port scanning (Nmap integration)
- Service analysis + CVE lookup
- Wireless security (WiFi/Bluetooth/IoT)
- Traffic analysis (PCAP parsing)
- MITM testing
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

### 🤖 Multi-Agent System
- Recon Agent
- Exploit Agent
- Defense Agent
- Coordinator
- Inter-agent communication

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
- Progressive training

---

## 📋 Prerequisites

### Common Requirements
- **Python 3.8+** (for Python-based implementations)
- **Ollama** (for AI features)

### Optional Requirements
- **Docker** (for Docker implementations)
- **Node.js** (for Web UI)
- **Claude Desktop** (for MCP stdio)

### Install Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.1:8b

# For more complex analysis
ollama pull llama3.1:70b
```

---

## 📚 Documentation

### Implementation Guides
- **[Standalone](implementations/standalone/README.md)** - CLI tool for local use
- **[MCP stdio](implementations/mcp-stdio/README.md)** - Claude Desktop integration
- **[MCP HTTP](implementations/mcp-http/README.md)** - Remote MCP server
- **[Web UI Full](implementations/web-ui-full/README.md)** - Complete web interface
- **[Docker Dev](implementations/docker-dev/README.md)** - Development environment
- **[Docker Production](implementations/docker-production/README.md)** - Production deployment
- **[Live USB](implementations/live-usb/README.md)** - Bootable USB

### General Documentation
- **[Features Complete](docs/FEATURES.md)** - Complete feature list
- **[Quick Start IT](docs/QUICK_START_IT.md)** - Quick start guide (Italian)
- **[Navigation Guide](docs/NAVIGATION.md)** - Navigate the new structure
- **[API Reference](docs/api.md)** - API documentation
- **[Training Guide](docs/TRAINING.md)** - LLM training system
- **[Contributing](docs/contributing.md)** - How to contribute

---

## 🏗️ Project Structure

```
Sec-llama/
├── implementations/           # 7 independent implementations
│   ├── standalone/           # CLI tool
│   ├── mcp-stdio/           # MCP for Claude Desktop
│   ├── mcp-http/            # MCP remote server
│   ├── web-ui-full/         # Complete Web UI
│   ├── docker-dev/          # Development environment
│   ├── docker-production/   # Production stack
│   └── live-usb/            # Bootable USB
│
├── shared/                   # Shared libraries
│   ├── core/                # Core security modules
│   ├── ai/                  # AI/LLM integration
│   └── utils/               # Common utilities
│
└── docs/                     # Documentation
```

**Note:** Each implementation is completely independent and self-contained. You can use one or multiple implementations based on your needs.

---

## 🔧 Configuration

### Remote Ollama Setup

If you want to use Ollama on a different machine:

**On the Ollama server:**
```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

**In Sec-Llama:**

For Web UI implementations:
1. Open Web UI → AI Configuration
2. Set host: `http://SERVER_IP:11434`
3. Test connection
4. Save

For other implementations, edit `config.yaml`:
```yaml
ollama:
  host: http://SERVER_IP:11434
  timeout: 120
  enabled: true
```

---

## 🐳 Docker Quick Reference

### Docker Dev
```bash
cd implementations/docker-dev
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Docker Production (Stack)
```bash
cd implementations/docker-production
./install.sh                                    # Install
docker stack services sec-llama                 # Check services
docker service logs -f sec-llama_web-ui        # View logs
docker service scale sec-llama_web-ui=3        # Scale
docker stack rm sec-llama                      # Remove
```

---

## 📊 Example Commands

### Network Security
```bash
# Discover hosts
./sec-llama.sh scan network 192.168.1.0/24

# AI-powered port scanning
./sec-llama.sh scan ports --host 192.168.1.10 --ai-suggest

# Vulnerability assessment
./sec-llama.sh scan vuln --network 192.168.1.0/24

# Analyze network traffic
./sec-llama.sh analyze traffic --pcap capture.pcap
```

### Application Security
```bash
# SAST code scanning
./sec-llama.sh scan code --path ./myapp --language python

# Container security
./sec-llama.sh scan container --image nginx:latest

# API fuzzing
./sec-llama.sh fuzz api --url https://api.example.com
```

### Threat Intelligence
```bash
# CVE lookup
./sec-llama.sh threat cve CVE-2024-1234

# IOC analysis
./sec-llama.sh threat ioc 192.168.1.100

# Search CVEs
./sec-llama.sh threat search --keyword "apache"
```

### LLM Training
```bash
# Collect training data
./sec-llama.sh train collect --type cve --max 10000

# Fine-tune model
./sec-llama.sh train finetune \
  --base llama3.1:8b \
  --dataset training_data.json \
  --name sec-llama-8b

# Evaluate model
./sec-llama.sh train evaluate --model sec-llama-8b
```

---

## ⚖️ Legal & Ethics

**IMPORTANT:** This tool is intended ONLY for:
- ✅ Authorized security testing
- ✅ CTF competitions
- ✅ Security research
- ✅ Personal test/lab environments
- ✅ Educational purposes

**DO NOT use for:**
- ❌ Unauthorized access to systems
- ❌ Illegal activities
- ❌ Testing without explicit permission

Users are responsible for appropriate use of this software.

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

- **Ollama**: Local LLM runtime
- **FastAPI**: Modern web framework
- **Vue.js**: Progressive JavaScript framework
- **Nmap**: Network scanning
- **Docker**: Containerization
- Community open source security tools

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)
- **Documentation**: [docs/](docs/)

---

## 🚀 Getting Started

1. **Choose an implementation** from the table above
2. **Follow the Quick Start** for that implementation
3. **Configure Ollama** (local or remote)
4. **Start testing!**

---

Made with ❤️ for the cybersecurity community

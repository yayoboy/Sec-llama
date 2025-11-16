# 🛡️ Sec-Llama LAN Server

**Complete cybersecurity testing platform for LAN deployment with remote LLM support**

This is the **unified implementation** of Sec-Llama designed specifically for:
- ✅ LAN server deployment
- ✅ Docker container orchestration
- ✅ Portainer management
- ✅ Remote LLM (Ollama or LM Studio on another PC)
- ✅ Web UI for complete management

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation Methods](#-installation-methods)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Security Modules](#-security-modules)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)

---

## 🎯 Features

### Core Capabilities
- **Remote LLM Integration**: Supports Ollama and LM Studio on separate machines
- **Web UI**: Complete management interface for configuration and operations
- **Docker-Ready**: Full Docker Compose and Portainer support
- **LAN Deployment**: Optimized for local network deployment
- **PostgreSQL + Redis**: Production-grade database and caching

### Security Modules
- **Network Security**: Host discovery, port scanning, traffic analysis, wireless auditing
- **Application Security**: SAST, code review, dependency scanning, container security
- **Threat Intelligence**: CVE lookup, IOC analysis, OSINT
- **Penetration Testing**: Exploit suggestions, attack planning, payload crafting
- **Incident Response**: IR automation, NIST playbooks, containment strategies
- **Log Analysis**: Multi-format parsing, anomaly detection, attack detection
- **Reporting**: Executive reports, technical reports, PDF/HTML export

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LAN Network                          │
│                                                         │
│  ┌──────────────┐     ┌──────────────┐                │
│  │ Remote LLM   │     │ LAN Server   │                │
│  │              │     │              │                │
│  │ • Ollama     │────▶│ • Web UI     │                │
│  │   OR         │     │ • PostgreSQL │                │
│  │ • LM Studio  │     │ • Redis      │                │
│  │              │     │ • Modules    │                │
│  └──────────────┘     └──────────────┘                │
│  192.168.1.100        192.168.1.10                     │
│  :11434 or :1234      :8080                            │
│                                                         │
│  ┌──────────────────────────────────┐                 │
│  │   Clients (Browsers)             │                 │
│  │   Access Web UI at :8080         │                 │
│  └──────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

**Components**:
1. **Remote LLM Server**: Ollama or LM Studio running on dedicated PC
2. **LAN Server**: Docker containers (Web UI, PostgreSQL, Redis)
3. **Clients**: Access via web browser to port 8080

---

## 📋 Prerequisites

### Required
- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Network**: LAN connectivity to LLM server
- **Ports**: 8080 (Web UI), 5432 (PostgreSQL), 6379 (Redis)

### Remote LLM Server (on another PC)
Choose one:

**Option 1: Ollama**
```bash
# On the LLM server PC
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.1:8b

# Start Ollama with network access
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

**Option 2: LM Studio**
1. Download from [https://lmstudio.ai/](https://lmstudio.ai/)
2. Load a model
3. Start local server (Settings → Enable API server)
4. Default: `http://localhost:1234`

### Optional
- **Portainer** (for Docker management UI)
- **Reverse Proxy** (Nginx/Traefik for HTTPS)

---

## 🚀 Quick Start

### Method 1: Docker Compose (Recommended)

```bash
# 1. Clone or navigate to lan-server directory
cd implementations/lan-server

# 2. Create .env file
cp .env.example .env

# 3. Edit .env - IMPORTANT: Configure these
nano .env  # or your preferred editor
# Set:
# - LLM_PROVIDER=ollama (or lm-studio)
# - OLLAMA_HOST=http://192.168.1.100:11434
# - SECRET_KEY=<random-string>
# - POSTGRES_PASSWORD=<secure-password>

# 4. Start services
docker-compose up -d

# 5. Check logs
docker-compose logs -f web-ui

# 6. Access Web UI
# Open browser: http://localhost:8080
```

### Method 2: Portainer Stack

```bash
# 1. Access Portainer UI
# Open: http://your-portainer-server:9000

# 2. Go to Stacks → Add Stack
# - Name: sec-llama-lan

# 3. Upload portainer-stack.yml
# Or copy/paste the content from the file

# 4. Add environment variables
# Copy from portainer-env.txt and add to Portainer
# IMPORTANT: Change all passwords and secrets!

# 5. Deploy stack

# 6. Access Web UI
# http://your-server-ip:8080
```

---

## 🔧 Configuration

### Environment Variables

The `.env` file contains all configuration. **Critical settings**:

```bash
# ===== LLM Configuration =====
LLM_PROVIDER=ollama                          # or 'lm-studio'
OLLAMA_HOST=http://192.168.1.100:11434      # Your Ollama server
OLLAMA_MODEL=llama3.1:8b                     # Model to use

# For LM Studio:
# LLM_PROVIDER=lm-studio
# LM_STUDIO_HOST=http://192.168.1.100:1234
# LM_STUDIO_MODEL=your-model-name

# ===== Security (CHANGE THESE!) =====
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-min-32-chars
POSTGRES_PASSWORD=your-secure-database-password
REDIS_PASSWORD=your-secure-redis-password

# ===== Network =====
WEB_UI_PORT=8080
POSTGRES_PORT=5432
REDIS_PORT=6379

# ===== CORS =====
ALLOWED_ORIGINS=*                            # For production: specific domains
```

### Remote LLM Setup

#### Ollama Server Configuration

On the **LLM server** (another PC):

```bash
# Method 1: Environment variable
export OLLAMA_HOST=0.0.0.0:11434
ollama serve

# Method 2: Systemd service (persistent)
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo '[Service]' | sudo tee /etc/systemd/system/ollama.service.d/override.conf
echo 'Environment="OLLAMA_HOST=0.0.0.0:11434"' | sudo tee -a /etc/systemd/system/ollama.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Verify
curl http://localhost:11434/api/tags
```

#### LM Studio Configuration

1. Open LM Studio
2. Go to Settings → Server
3. Enable "Start server automatically"
4. Set "Server Host": `0.0.0.0`
5. Set "Server Port": `1234`
6. Click "Start Server"

#### Test Connection

```bash
# From LAN server, test connection to LLM

# For Ollama:
curl http://192.168.1.100:11434/api/tags

# For LM Studio:
curl http://192.168.1.100:1234/v1/models
```

---

## 💻 Usage

### Web UI

Access the Web UI at `http://your-server-ip:8080`

**Features**:
1. **Dashboard**: Real-time statistics and system status
2. **AI Configuration**: Configure and test remote LLM connection
3. **Security Tools**: Execute scans and assessments
4. **Reports**: View and export security reports
5. **API Keys**: Manage authentication keys
6. **Audit Logs**: View system activity logs

### Web UI Sections

#### 1. Dashboard
- System status (PostgreSQL, Redis, LLM)
- Recent activity
- Quick actions

#### 2. AI Configuration
- Configure LLM provider (Ollama/LM Studio)
- Test connection
- Change models
- View available models

#### 3. Security Tools

**Network Security**:
- Host Discovery: `POST /api/tools/network/discover`
- Port Scanning: `POST /api/tools/network/scan`
- Traffic Analysis: `POST /api/tools/network/traffic`

**Vulnerability Assessment**:
- Code Scanning: `POST /api/tools/code/scan`
- Container Security: `POST /api/tools/container/scan`

**Threat Intelligence**:
- CVE Lookup: `POST /api/tools/threat/cve`
- IOC Analysis: `POST /api/tools/threat/ioc`

#### 4. Reports
- View generated reports
- Export as PDF/HTML/JSON
- Schedule automated reports

---

## 🔒 Security Modules

All modules support AI-enhanced analysis via remote LLM.

### Network Security
| Module | Description |
|--------|-------------|
| Host Discovery | ARP/ICMP/TCP discovery |
| Port Scanner | AI-enhanced Nmap integration |
| Traffic Analyzer | PCAP analysis with AI insights |
| Wireless Auditor | WiFi/Bluetooth security |

### Application Security
| Module | Description |
|--------|-------------|
| Code Scanner | SAST for Python, JS, Java, Go, PHP |
| Container Scanner | Docker/Kubernetes security |
| API Fuzzer | REST/GraphQL testing |
| Dependency Scanner | Vulnerability detection |

### Threat Intelligence
| Module | Description |
|--------|-------------|
| CVE Lookup | NVD integration with AI analysis |
| IOC Analyzer | Malicious indicator detection |
| OSINT | Open source intelligence |

### Incident Response
| Module | Description |
|--------|-------------|
| IR Orchestrator | Automated incident response |
| Playbooks | NIST-based response plans |
| Containment | Threat isolation strategies |

---

## 🐛 Troubleshooting

### Cannot connect to LLM server

```bash
# Check if LLM server is accessible
ping 192.168.1.100

# Test LLM API
curl http://192.168.1.100:11434/api/tags  # Ollama
curl http://192.168.1.100:1234/v1/models  # LM Studio

# Check firewall on LLM server
sudo ufw status
sudo ufw allow 11434  # For Ollama
sudo ufw allow 1234   # For LM Studio
```

### Web UI not accessible

```bash
# Check if container is running
docker-compose ps

# Check logs
docker-compose logs web-ui

# Check port binding
docker port sec-llama-web-ui
```

### Database connection issues

```bash
# Check PostgreSQL
docker-compose logs postgres

# Test connection
docker exec -it sec-llama-postgres psql -U sec_llama -d sec_llama
```

### Permission denied errors

```bash
# Fix directory permissions
sudo chown -R 1000:1000 logs/ reports/ database/
```

---

## 📊 API Reference

### Health Check

```bash
GET /api/health

Response:
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "llm": "connected"
}
```

### LLM Test

```bash
POST /api/llm/test

Response:
{
  "status": "ok",
  "provider": "ollama",
  "host": "http://192.168.1.100:11434",
  "models": ["llama3.1:8b", "mistral:latest"],
  "current_model": "llama3.1:8b"
}
```

### Network Scan

```bash
POST /api/tools/network/scan
Content-Type: application/json

{
  "network": "192.168.1.0/24",
  "scan_type": "quick",
  "ai_analysis": true
}

Response:
{
  "scan_id": "abc123",
  "status": "completed",
  "hosts_found": 15,
  "report_url": "/api/reports/abc123"
}
```

---

## 📁 Directory Structure

```
lan-server/
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Web UI container image
├── .env.example            # Environment variables template
├── .env                    # Your configuration (create this)
├── portainer-stack.yml     # Portainer stack file
├── portainer-env.txt       # Portainer environment variables
├── requirements.txt        # Python dependencies
├── setup.sh                # Local setup script
├── README.md              # This file
│
├── core/                   # Core modules
│   ├── config.py          # Configuration management
│   ├── llm_interface.py   # LLM integration (Ollama/LM Studio)
│   └── prompt_templates.py # AI prompt templates
│
├── modules/               # Security modules
│   ├── network/          # Network security tools
│   ├── threat_intel/     # Threat intelligence
│   ├── code_review/      # Code analysis
│   ├── vuln_scanner/     # Vulnerability scanning
│   ├── container_security/ # Container scanning
│   ├── api_security/     # API security
│   ├── log_analyzer/     # Log analysis
│   ├── incident_response/ # IR automation
│   ├── pentest_assistant/ # Pentest planning
│   ├── training/         # LLM training
│   └── reporting/        # Report generation
│
├── web_ui/               # Web interface
│   ├── backend/         # FastAPI backend
│   └── frontend/        # Vue.js frontend
│
├── config/              # Configuration files
├── logs/                # Application logs
├── reports/             # Generated reports
└── database/            # Local database files
```

---

## 🔄 Maintenance

### Update Images

```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose up -d
```

### Backup Database

```bash
# Backup PostgreSQL
docker exec sec-llama-postgres pg_dump -U sec_llama sec_llama > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20240101.sql | docker exec -i sec-llama-postgres psql -U sec_llama -d sec_llama
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web-ui

# Last 100 lines
docker-compose logs --tail=100 web-ui
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

---

## 🆘 Support

- **Documentation**: See `/docs` for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Community**: Join discussions

---

## 📄 License

MIT License - see LICENSE file

---

## 🙏 Credits

- **Ollama**: Local LLM runtime
- **LM Studio**: Local LLM interface
- **FastAPI**: Modern web framework
- **PostgreSQL**: Database
- **Redis**: Caching
- **Docker**: Containerization

---

Made with ❤️ for the cybersecurity community

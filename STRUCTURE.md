# 📁 Project Structure

Sec-Llama is organized into logical modules for easy navigation and maintenance.

## 🗂️ Directory Structure

```
Sec-llama/
│
├── 🚀 deployments/          # Deployment configurations
│   ├── docker/              # Docker Compose files
│   ├── docker-stack/        # Docker Stack (production)
│   └── live-usb/           # Live USB creation scripts
│
├── 🛡️ core/                 # Core security modules
│   ├── network/            # Network security
│   ├── code_analysis/      # SAST and code review
│   ├── threat_intel/       # Threat intelligence
│   ├── web_security/       # Web app security
│   ├── exploit/            # Penetration testing
│   ├── incident_response/  # IR automation
│   ├── log_analyzer/       # Log analysis
│   ├── reporting/          # Report generation
│   └── container_security/ # Container/K8s security
│
├── 🔌 mcp-server/           # MCP Server implementation
│   ├── server.py           # Main server
│   ├── transports/         # Stdio & HTTP transports
│   └── tools/              # MCP tool implementations
│
├── 🎨 web-ui/               # Web User Interface
│   ├── backend/            # FastAPI backend
│   └── frontend/           # Vue.js frontend
│
├── 🤖 ai/                   # AI & Machine Learning
│   ├── llm/                # LLM integration
│   ├── prompts/            # Prompt templates
│   └── training/           # Model fine-tuning
│
├── 💻 cli/                  # Command-line interface
│
├── 🔧 scripts/              # Utility scripts
│   ├── install_stack.sh    # Docker Stack installer
│   ├── start_web_ui.sh     # Web UI starter
│   └── build_web_ui.sh     # Frontend builder
│
├── ⚙️ config/               # Global configurations
│
├── 📚 docs/                 # Documentation
│   ├── DOCKER_STACK_INSTALLATION.md
│   ├── WEB_UI_GUIDE.md
│   ├── MCP_SERVER_GUIDE.md
│   └── ...
│
└── 🧪 tests/                # Test suites
```

## 📖 Module Descriptions

### 🚀 Deployments

Everything related to deploying Sec-Llama in different environments.

- **`docker/`**: Standard Docker Compose for development
- **`docker-stack/`**: Production Docker Swarm deployment
- **`live-usb/`**: Scripts for creating bootable security testing USB

**Use when:** You want to deploy or run Sec-Llama

**See:** [deployments/README.md](deployments/README.md)

---

### 🛡️ Core

Core security testing modules - the heart of Sec-Llama.

Each subdirectory is a self-contained security module:

- **`network/`**: Network discovery, scanning, traffic analysis
- **`code_analysis/`**: SAST, dependency scanning, secret detection
- **`threat_intel/`**: CVE lookup, MITRE ATT&CK, IOC checking
- **`web_security/`**: OWASP Top 10, XSS, SQLi, API testing
- **`exploit/`**: Penetration testing tools and automation
- **`incident_response/`**: IR workflows and automation
- **`log_analyzer/`**: Log analysis and correlation
- **`reporting/`**: Automated report generation
- **`container_security/`**: Docker/K8s security scanning

**Use when:** You want to use security tools programmatically

**See:** [core/README.md](core/README.md)

---

### 🔌 MCP Server

Model Context Protocol server for tool access.

Provides two ways to access security tools:
1. **Local (stdio)**: For Claude Desktop integration
2. **Remote (HTTP/SSE)**: For LAN/remote access

**Use when:** You want to expose tools via MCP protocol

**See:** [mcp-server/README.md](mcp-server/README.md)

---

### 🎨 Web UI

Modern web interface for Sec-Llama.

- **`backend/`**: FastAPI REST API
- **`frontend/`**: Vue.js 3 SPA

**Features:**
- Dashboard with real-time stats
- Tool execution interface
- AI configuration (Ollama remote/local)
- API key management
- Audit logs viewer

**Use when:** You want a graphical interface

**See:** [web-ui/README.md](web_ui/README.md)

---

### 🤖 AI

AI and machine learning components.

- **`llm/`**: LLM interface (Ollama, OpenAI, Claude, etc.)
- **`prompts/`**: Security-specific prompt templates
- **`training/`**: Model fine-tuning for security tasks

**Use when:** You want to integrate or train AI models

**See:** [ai/README.md](ai/README.md)

---

### 💻 CLI

Command-line interface for standalone use.

**Use when:** You prefer terminal-based interaction

---

### 🔧 Scripts

Utility scripts for installation, setup, and maintenance.

**Key scripts:**
- `install_stack.sh` - One-command Docker Stack installation
- `start_web_ui.sh` - Start Web UI (dev or prod mode)
- `build_web_ui.sh` - Build frontend for production

---

### ⚙️ Config

Global configuration files.

- `mcp_server_config.yaml` - MCP Server configuration
- Environment-specific configs

---

### 📚 Docs

Comprehensive documentation.

**Key documents:**
- `DOCKER_STACK_INSTALLATION.md` - Complete installation guide
- `WEB_UI_GUIDE.md` - Web UI user guide
- `MCP_SERVER_GUIDE.md` - MCP Server setup
- `TRAINING.md` - AI training guide
- `FEATURES.md` - Complete features list

---

## 🎯 Common Use Cases

### I want to deploy Sec-Llama in production
→ Go to [`deployments/docker-stack/`](deployments/docker-stack/)
→ Run `../../scripts/install_stack.sh`

### I want to use security tools programmatically
→ Import from [`core/`](core/)
→ Example: `from core.network.discovery import HostDiscovery`

### I want to access tools via MCP
→ Use [`mcp-server/`](mcp-server/)
→ See [MCP Server Guide](docs/MCP_SERVER_GUIDE.md)

### I want a web interface
→ Start [`web-ui/`](web_ui/)
→ Run `./scripts/start_web_ui.sh`

### I want to configure AI (Ollama remote/local)
→ Open Web UI: http://localhost:8080/ai-config
→ Or edit `config/mcp_server_config.yaml`

### I want to train custom models
→ Use [`ai/training/`](ai/training/)
→ See [Training Guide](docs/TRAINING.md)

### I want to develop locally
→ Use [`deployments/docker/`](deployments/docker/)
→ Run `docker-compose up -d`

---

## 🔄 Migration from Old Structure

The project was reorganized for clarity. Here's the mapping:

**Old** → **New**

- `docker-compose.yml` → `deployments/docker/`
- `docker-stack.yml` → `deployments/docker-stack/`
- `modules/network/` → `core/network/`
- `modules/code_review/` → `core/code_analysis/`
- `modules/training/` → `ai/training/`
- `mcp_server/` → `mcp-server/`
- Live USB scripts → `deployments/live-usb/`

**Import changes:**
```python
# Old
from modules.network.discovery import HostDiscovery

# New
from core.network.discovery import HostDiscovery
```

---

## 📊 Quick Reference

| What I want to do | Where to go |
|-------------------|-------------|
| Deploy in production | `deployments/docker-stack/` |
| Develop locally | `deployments/docker/` |
| Use security tools | `core/` |
| MCP integration | `mcp-server/` |
| Web interface | `web-ui/` |
| Configure AI | `ai/` or Web UI |
| Train models | `ai/training/` |
| Read docs | `docs/` |

---

**Need help?** Check the README in each directory or the main [documentation](docs/).

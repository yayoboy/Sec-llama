# 🖥️ Sec-Llama Web UI - Complete Guide

Complete guide for using the Sec-Llama Web UI configuration and management interface.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Development Mode](#development-mode)
   - [Production Mode](#production-mode)
5. [Components](#components)
6. [API Reference](#api-reference)
7. [Docker Deployment](#docker-deployment)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The Sec-Llama Web UI provides a modern, intuitive interface for managing and configuring the Sec-Llama MCP Server. Built with Vue.js 3 and FastAPI, it offers real-time monitoring, tool execution, and configuration management.

### Key Features

- ✅ **Real-time Dashboard** with system statistics
- ✅ **Tool Execution Interface** with dynamic form generation
- ✅ **Configuration Editor** with YAML validation
- ✅ **API Key Management** with usage tracking
- ✅ **Audit Logs Viewer** with filtering and export
- ✅ **WebSocket Support** for live updates
- ✅ **Responsive Design** with Tailwind CSS
- ✅ **Docker Ready** for easy deployment

---

## ✨ Features

### Dashboard

- **System Statistics**: Real-time metrics for executions, active tasks, and system health
- **Recent Executions**: View recent tool executions with status and duration
- **Top Tools**: Visualize most-used tools with success rates
- **Execution Charts**: Hourly execution trends

### Tools Execution

- **Tool Browser**: Browse available security tools by category
- **Dynamic Forms**: Automatically generated parameter forms from tool schemas
- **Example Loading**: Quick parameter filling with provided examples
- **Real-time Results**: View execution results as they complete
- **Export Results**: Download execution results for reporting

### Configuration Editor

- **YAML Editor**: Edit MCP server configuration directly
- **Validation**: Real-time YAML syntax and schema validation
- **Backup & Restore**: Create and restore configuration backups
- **Schema Helper**: View configuration schema for guidance
- **Download**: Export current configuration

### API Key Management

- **Create Keys**: Generate new API keys with custom permissions
- **Revoke/Activate**: Manage key lifecycle
- **Usage Tracking**: View key usage statistics
- **Secure Display**: Keys shown only once during creation

### Audit Logs

- **Log Viewer**: Browse all tool execution logs
- **Advanced Filtering**: Filter by tool, status, date range
- **Statistics**: View aggregated log statistics
- **Export**: Export logs in JSON or CSV format
- **Details View**: Inspect full execution details

---

## 📥 Installation

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm (for frontend development)
- **Ollama** (optional, for LLM features)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama
```

### Step 2: Install Backend Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies (Development Only)

```bash
cd web_ui/frontend
npm install
cd ../..
```

### Step 4: Build Frontend for Production

```bash
./scripts/build_web_ui.sh
```

---

## 🚀 Usage

### Development Mode

Run backend and frontend separately with hot-reload:

```bash
./scripts/start_web_ui.sh --mode development
```

This starts:
- **Backend**: http://localhost:8080 (FastAPI with auto-reload)
- **Frontend**: http://localhost:3000 (Vue dev server with HMR)

### Production Mode

Run with built frontend served from backend:

```bash
# Build frontend first (if not already built)
./scripts/build_web_ui.sh

# Start Web UI
./scripts/start_web_ui.sh --mode production
```

Access at: **http://localhost:8080**

### Backend Only

Start only the backend server:

```bash
./scripts/start_web_ui.sh --backend-only
```

### Custom Ports

```bash
# Custom backend port
./scripts/start_web_ui.sh --mode production --backend-port 9000

# Custom ports in development
./scripts/start_web_ui.sh --mode development --backend-port 9000 --frontend-port 4000
```

---

## 🧩 Components

### Backend (FastAPI)

**Location**: `web_ui/backend/`

#### Main Application

- `main.py`: FastAPI application with CORS, router registration
- `routers/`: API route handlers
  - `dashboard.py`: Dashboard statistics and metrics
  - `tools.py`: Tool listing and execution
  - `config.py`: Configuration management
  - `api_keys.py`: API key CRUD operations
  - `audit_logs.py`: Log querying and export
  - `websocket.py`: WebSocket event streaming

#### Models

- `models/`: Pydantic models for request/response validation
  - `tool.py`: Tool execution models
  - `config.py`: Configuration models
  - `api_key.py`: API key models
  - `dashboard.py`: Dashboard data models

#### Services

- `services/tool_executor.py`: Tool execution service with history tracking

### Frontend (Vue.js 3)

**Location**: `web_ui/frontend/`

#### Core Files

- `src/main.js`: Application entry point
- `src/App.vue`: Root component
- `src/router/index.js`: Vue Router configuration
- `src/api/client.js`: Axios API client

#### Views

- `DashboardView.vue`: Main dashboard with statistics
- `ToolsView.vue`: Tool browser and execution interface
- `ConfigView.vue`: Configuration editor
- `ApiKeysView.vue`: API key management
- `AuditLogsView.vue`: Audit log viewer

#### Stores (Pinia)

- `stores/dashboard.js`: Dashboard state management
- `stores/tools.js`: Tools and execution state
- `stores/websocket.js`: WebSocket connection management

#### Components

- `DashboardLayout.vue`: Main layout with sidebar navigation

---

## 📚 API Reference

### Base URL

```
http://localhost:8080/api
```

### Endpoints

#### Dashboard

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | Get complete dashboard data |
| `/dashboard/stats` | GET | Get system statistics |
| `/dashboard/recent-executions` | GET | Get recent executions |
| `/dashboard/tool-usage` | GET | Get tool usage statistics |

#### Tools

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tools` | GET | List all tools |
| `/tools/{tool_name}` | GET | Get tool info |
| `/tools/{tool_name}/execute` | POST | Execute tool |
| `/tools/executions/{id}` | GET | Get execution status |
| `/tools/history` | GET | Get execution history |

#### Configuration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/config` | GET | Get configuration |
| `/config` | PUT | Update configuration |
| `/config/validate` | POST | Validate configuration |
| `/config/backup` | POST | Create backup |
| `/config/backups` | GET | List backups |
| `/config/restore/{id}` | POST | Restore backup |

#### API Keys

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api-keys` | GET | List API keys |
| `/api-keys` | POST | Create API key |
| `/api-keys/{id}` | GET | Get API key info |
| `/api-keys/{id}` | PATCH | Update API key |
| `/api-keys/{id}` | DELETE | Delete API key |
| `/api-keys/{id}/revoke` | POST | Revoke API key |
| `/api-keys/{id}/usage` | GET | Get usage stats |

#### Audit Logs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/audit-logs` | GET | Get audit logs |
| `/audit-logs/stats` | GET | Get log statistics |
| `/audit-logs/export` | GET | Export logs |

#### WebSocket

| Endpoint | Protocol | Description |
|----------|----------|-------------|
| `/ws/events` | WebSocket | General event stream |
| `/ws/dashboard` | WebSocket | Dashboard updates |

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Build and start Web UI
docker-compose -f docker-compose.web-ui.yml up -d

# View logs
docker-compose -f docker-compose.web-ui.yml logs -f sec-llama-web-ui

# Access Web UI
# http://localhost:8080
```

### With MCP Server

To run both Web UI and MCP Server:

```bash
# Start with MCP server profile
docker-compose -f docker-compose.web-ui.yml --profile with-mcp up -d

# This starts:
# - Web UI on port 8080
# - MCP Server on port 8765
# - Ollama on port 11434
```

### Environment Variables

```bash
# Set environment variables
export MCP_API_KEYS="your_api_key_here"
export LOG_LEVEL="INFO"

# Start with environment
docker-compose -f docker-compose.web-ui.yml up -d
```

### Stop Services

```bash
docker-compose -f docker-compose.web-ui.yml down

# Remove volumes (careful!)
docker-compose -f docker-compose.web-ui.yml down -v
```

---

## ⚙️ Configuration

### Frontend Configuration

**File**: `web_ui/frontend/vite.config.js`

```javascript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
})
```

### Backend Configuration

The Web UI backend uses the same configuration as the MCP server:

**File**: `config/mcp_server_config.yaml`

Relevant sections:
- `server`: Server identification
- `ollama`: LLM configuration
- `security`: Access control settings

---

## 🔧 Troubleshooting

### Frontend Won't Build

```bash
# Clear node_modules and reinstall
cd web_ui/frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Backend API Errors

```bash
# Check backend logs
tail -f logs/mcp_server.log

# Verify dependencies
pip list | grep fastapi
pip list | grep uvicorn
```

### WebSocket Connection Issues

1. **Check CORS settings** in `main.py`
2. **Verify WebSocket URL** in frontend (check protocol: ws:// vs wss://)
3. **Check firewall rules** for WebSocket traffic

### Docker Build Fails

```bash
# Check Docker daemon
docker info

# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose -f docker-compose.web-ui.yml build --no-cache
```

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
./scripts/start_web_ui.sh --backend-port 9000
```

---

## 📸 Screenshots

### Dashboard
- System statistics cards
- Recent executions table
- Tool usage charts

### Tool Execution
- Tool cards by category
- Dynamic parameter forms
- Real-time execution results

### Configuration
- YAML editor with syntax highlighting
- Validation errors and warnings
- Backup management

### API Keys
- Key listing with status
- Secure key creation
- Usage statistics

---

## 🔗 Additional Resources

- **Main Documentation**: [README.md](../README.md)
- **MCP Server Guide**: [MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md)
- **Feature List**: [FEATURES.md](FEATURES.md)
- **Training Guide**: [TRAINING.md](TRAINING.md)

---

## 🆘 Support

**Issues**: [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
**Discussions**: [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)

---

**Made with ❤️ by the Sec-Llama Team**

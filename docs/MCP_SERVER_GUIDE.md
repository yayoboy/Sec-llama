# 🔌 Sec-Llama MCP Server - Complete Guide

Complete guide for setting up and using the Sec-Llama Model Context Protocol (MCP) Server.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [What is MCP?](#what-is-mcp)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
   - [Local Usage (stdio)](#local-usage-stdio)
   - [LAN Usage (HTTP/SSE)](#lan-usage-httpsse)
7. [Available Tools](#available-tools)
8. [Docker Deployment](#docker-deployment)
9. [Security](#security)
10. [Troubleshooting](#troubleshooting)
11. [API Reference](#api-reference)

---

## 🎯 Overview

The Sec-Llama MCP Server exposes all security testing capabilities of Sec-Llama as **Model Context Protocol (MCP) tools**, making them accessible to Claude and other MCP-compatible AI assistants.

### Key Features

- ✅ **8+ Security Tools** exposed via MCP
- ✅ **Dual Transport**: stdio (local) and HTTP/SSE (LAN)
- ✅ **API Key Authentication** for secure remote access
- ✅ **Rate Limiting** to prevent abuse
- ✅ **Audit Logging** for compliance
- ✅ **Docker Support** for easy deployment
- ✅ **100% Local** - no external dependencies

### Use Cases

- **Claude Desktop Integration**: Use security tools directly from Claude Desktop
- **LAN Server**: Deploy centralized security testing server for team
- **Automation**: Integrate with scripts and workflows
- **Multi-user**: Share security capabilities across organization

---

## 🔍 What is MCP?

**Model Context Protocol (MCP)** is an open protocol developed by Anthropic that allows AI assistants to securely interact with external tools and data sources.

**Benefits:**
- Standardized way for LLMs to call external tools
- Secure, type-safe parameter passing
- Works with Claude Desktop, Claude API, and other MCP clients
- Easy to extend with new capabilities

**Learn more:** [Model Context Protocol Documentation](https://modelcontextprotocol.io)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   MCP Client (Claude Desktop/API)   │
│                                     │
│  - Sends tool requests              │
│  - Receives structured results      │
└──────────────┬──────────────────────┘
               │
               │ MCP Protocol
               │ (stdio or HTTP/SSE)
               │
┌──────────────▼──────────────────────┐
│    Sec-Llama MCP Server             │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  MCP Tools Registry          │  │
│  │  - network_discover          │  │
│  │  - network_scan              │  │
│  │  - code_scan                 │  │
│  │  - threat_cve_lookup         │  │
│  │  - threat_ioc_analyze        │  │
│  │  - ...and more               │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Transport Layer             │  │
│  │  - stdio (local)             │  │
│  │  - HTTP/SSE (LAN)            │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Security Layer              │  │
│  │  - API Key Auth              │  │
│  │  - Rate Limiting             │  │
│  │  - Audit Logging             │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Sec-Llama Core Modules           │
│                                     │
│  - Network Security                 │
│  - Code Analysis                    │
│  - Threat Intelligence              │
│  - Ollama LLM Integration           │
└─────────────────────────────────────┘
```

---

## 📥 Installation

### Prerequisites

- **Python 3.8+**
- **Ollama** (for LLM capabilities)
- **Network tools** (nmap, masscan - optional)

### Step 1: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.1:8b
```

### Step 2: Install Sec-Llama MCP Server

```bash
# Clone repository
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-mcp.txt
```

### Step 3: Verify Installation

```bash
# Test stdio mode
python3 mcp_server/server.py --transport stdio
# Press Ctrl+C to exit

# Test HTTP mode
python3 mcp_server/server.py --transport http
# Visit: http://localhost:8765/health
```

---

## ⚙️ Configuration

### Configuration File

Main configuration: `config/mcp_server_config.yaml`

```yaml
# Server settings
server:
  name: "sec-llama"
  version: "1.0.0"

# Transport configuration
transport:
  stdio:
    enabled: true

  http:
    enabled: true
    host: "0.0.0.0"
    port: 8765

# Authentication
auth:
  type: "api_key"
  api_keys:
    - name: "admin"
      key: "your_api_key_here"
      permissions: ["*"]

# Rate limiting
rate_limiting:
  enabled: true
  default_limit: "100/hour"

# Security
security:
  require_confirmation: true
  allowed_networks:
    - "192.168.0.0/16"
    - "10.0.0.0/8"
```

### Environment Variables

Create `.env.mcp` from `.env.mcp.example`:

```bash
cp .env.mcp.example .env.mcp
nano .env.mcp
```

```bash
# Key environment variables
MCP_HOST=0.0.0.0
MCP_PORT=8765
MCP_API_KEYS=key1,key2,key3
OLLAMA_HOST=http://localhost:11434
```

### Generate API Keys

```bash
# Method 1: OpenSSL
openssl rand -hex 32

# Method 2: Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# Method 3: Online
# Visit: https://randomkeygen.com/
```

---

## 🚀 Usage

### Local Usage (stdio)

**Best for:** Claude Desktop, local CLI

#### Setup Claude Desktop

Use the automated installer:

```bash
./scripts/install_mcp_client.sh
```

Or manually edit Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sec-llama": {
      "command": "python3",
      "args": ["/path/to/Sec-llama/mcp_server/server.py", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "/path/to/Sec-llama",
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  }
}
```

#### Start Server

```bash
# Option 1: Use script
./scripts/start_mcp_server.sh stdio

# Option 2: Direct command
python3 mcp_server/server.py --transport stdio
```

#### Usage in Claude Desktop

```
You: Use network_discover to scan 192.168.1.0/24

Claude: I'll use the network_discover tool to scan your network...
[Executes tool and shows results]
```

---

### LAN Usage (HTTP/SSE)

**Best for:** Server deployment, team sharing, remote access

#### Start HTTP Server

```bash
# Option 1: Use script with API keys
MCP_API_KEYS='abc123,def456' ./scripts/start_mcp_server.sh http

# Option 2: Direct command
python3 mcp_server/server.py \
  --transport http \
  --host 0.0.0.0 \
  --port 8765 \
  --api-keys "your_api_key_here"
```

#### Access from Client

**Python Example:**

```python
import asyncio
from mcp.client import Client

async def main():
    # Connect to MCP server
    client = Client(
        "http://192.168.1.100:8765/sse",
        headers={"X-API-Key": "your_api_key_here"}
    )

    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        # Call network_discover tool
        result = await client.call_tool(
            "network_discover",
            {
                "subnet": "192.168.1.0/24",
                "method": "arp"
            }
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

**cURL Example:**

```bash
# Health check
curl http://192.168.1.100:8765/health

# List tools (with API key)
curl -H "X-API-Key: your_key" http://192.168.1.100:8765/tools

# SSE connection
curl -H "X-API-Key: your_key" \
     -H "Accept: text/event-stream" \
     http://192.168.1.100:8765/sse
```

---

## 🛠️ Available Tools

### Network Security Tools

#### `network_discover`

Discover hosts in a network subnet.

```json
{
  "subnet": "192.168.1.0/24",
  "method": "arp"  // arp, icmp, or tcp
}
```

**Returns:** List of active hosts with IP, MAC, hostname, vendor

#### `network_scan`

Intelligent port scanning with AI analysis.

```json
{
  "host": "192.168.1.100",
  "ports": "1-1000",  // optional
  "profile": "standard",  // quick, standard, thorough, stealth
  "ai_analysis": true
}
```

**Returns:** Open ports, services, versions, CVE matches, AI recommendations

#### `network_vuln_scan`

Comprehensive vulnerability scan.

```json
{
  "network": "192.168.1.0/24",
  "depth": "standard"  // quick, standard, full
}
```

**Returns:** Complete network assessment with vulnerabilities

### Code Security Tools

#### `code_scan`

SAST code analysis for vulnerabilities.

```json
{
  "path": "/path/to/code",
  "language": "python",  // auto, python, javascript, java, go, php
  "severity_filter": ["HIGH", "CRITICAL"],
  "include_ai_analysis": true
}
```

**Returns:** Security issues, CWE mappings, remediation advice

#### `code_dependency_check`

Check dependencies for known CVEs.

```json
{
  "project_path": "/path/to/project",
  "ecosystem": "auto"  // npm, pip, maven, go, auto
}
```

**Returns:** Vulnerable dependencies with CVE information

### Threat Intelligence Tools

#### `threat_cve_lookup`

Look up CVE information from NVD.

```json
{
  "cve_id": "CVE-2021-41773",
  "include_exploits": true,
  "include_ai_analysis": true
}
```

**Returns:** CVSS score, severity, exploits, remediation

#### `threat_ioc_analyze`

Analyze Indicators of Compromise.

```json
{
  "ioc": "192.168.1.100",
  "ioc_type": "auto",  // ip, domain, url, hash, email
  "context": "Found in suspicious log entry"
}
```

**Returns:** Threat classification, reputation, recommended actions

#### `threat_osint`

OSINT gathering (coming soon).

```json
{
  "target": "example.com",
  "osint_type": "all",  // domain, ip, email, organization
  "depth": "standard"
}
```

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Generate API keys
export MCP_API_KEYS=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Start services
docker-compose -f docker-compose.mcp.yml up -d

# Check logs
docker-compose -f docker-compose.mcp.yml logs -f sec-llama-mcp

# Pull model (first time)
docker-compose -f docker-compose.mcp.yml exec ollama ollama pull llama3.1:8b
```

### Access Server

```bash
# Health check
curl http://localhost:8765/health

# List tools
curl -H "X-API-Key: $MCP_API_KEYS" http://localhost:8765/tools
```

### Stop Services

```bash
docker-compose -f docker-compose.mcp.yml down

# Remove volumes (careful!)
docker-compose -f docker-compose.mcp.yml down -v
```

---

## 🔒 Security

### API Key Authentication

**Required for HTTP/SSE transport:**

```bash
# Start with API keys
python3 mcp_server/server.py \
  --transport http \
  --api-keys "key1,key2,key3"
```

**Client usage:**

```python
headers = {"X-API-Key": "your_key_here"}
```

### Rate Limiting

Configure in `config/mcp_server_config.yaml`:

```yaml
rate_limiting:
  enabled: true
  default_limit: "100/hour"

  tool_limits:
    network_scan: "30/hour"
    network_vuln_scan: "10/hour"
```

### Network ACL

Restrict access to specific networks:

```yaml
security:
  allowed_networks:
    - "192.168.1.0/24"  # Local network only
    - "10.0.0.0/8"

  blocked_ips:
    - "1.2.3.4"  # Block specific IPs
```

### Audit Logging

All tool executions are logged:

```bash
# View audit log
tail -f logs/mcp_audit.log

# Format: timestamp - api_key - tool - status - duration
2024-11-13 10:00:00 - admin_key - network_discover - success - 2.5s
```

### Best Practices

1. **Always use API keys** for HTTP transport
2. **Use strong, unique keys** (32+ characters)
3. **Rotate keys regularly** (monthly recommended)
4. **Restrict to LAN** (don't expose to internet)
5. **Enable rate limiting** to prevent abuse
6. **Monitor audit logs** for suspicious activity
7. **Use HTTPS** if exposing outside LAN (requires reverse proxy)

---

## 🔧 Troubleshooting

### Server Won't Start

```bash
# Check if port is already in use
lsof -i :8765

# Check Ollama is running
curl http://localhost:11434/api/tags

# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip list | grep mcp
```

### Claude Desktop Not Showing Tools

1. **Verify config location:**
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Linux
   cat ~/.config/claude/claude_desktop_config.json
   ```

2. **Check absolute paths** in config (no `~` or relative paths)

3. **Restart Claude Desktop** completely

4. **Check logs:**
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log

   # Linux
   journalctl --user -u claude-desktop -f
   ```

### Authentication Errors

```bash
# Verify API key format
echo "X-API-Key: your_key" | curl -H @- http://localhost:8765/tools

# Check server logs
tail -f logs/mcp_server.log | grep -i auth
```

### Performance Issues

```bash
# Check Ollama model size
ollama list

# Use smaller model
ollama pull llama3.1:8b-instruct-q4_K_M  # Quantized version

# Reduce concurrent requests
# Edit config/mcp_server_config.yaml:
# performance:
#   max_concurrent_requests: 2
```

### Docker Issues

```bash
# Check container logs
docker logs sec-llama-mcp-server

# Check Ollama container
docker logs sec-llama-ollama

# Restart containers
docker-compose -f docker-compose.mcp.yml restart

# Clean restart
docker-compose -f docker-compose.mcp.yml down
docker-compose -f docker-compose.mcp.yml up -d
```

---

## 📚 API Reference

### HTTP Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Server info |
| `/health` | GET | No | Health check |
| `/tools` | GET | Yes | List tools |
| `/sse` | POST | Yes | SSE connection |

### Tool Schemas

All tools follow JSON Schema format:

```json
{
  "name": "tool_name",
  "description": "What this tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Parameter description"
      }
    },
    "required": ["param1"]
  }
}
```

### Response Format

```json
{
  "type": "text",
  "text": "Markdown-formatted results with structured data"
}
```

---

## 🔗 Additional Resources

- **Main Documentation:** [README.md](../README.md)
- **Feature List:** [FEATURES.md](FEATURES.md)
- **Training Guide:** [TRAINING.md](TRAINING.md)
- **Dataset Guide:** [DATASETS_GUIDE.md](DATASETS_GUIDE.md)
- **Live USB Guide:** [LIVE_USB_GUIDE.md](LIVE_USB_GUIDE.md)
- **MCP Official Docs:** [modelcontextprotocol.io](https://modelcontextprotocol.io)

---

## 🆘 Support

**Issues:** [GitHub Issues](https://github.com/yourusername/Sec-llama/issues)
**Discussions:** [GitHub Discussions](https://github.com/yourusername/Sec-llama/discussions)

---

**Made with ❤️ by the Sec-Llama Team**

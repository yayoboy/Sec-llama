# MCP Server

Model Context Protocol (MCP) Server implementation for Sec-Llama.

Provides both local (stdio) and remote (HTTP/SSE) access to security tools.

## 📁 Structure

```
mcp-server/
├── server.py          # Main MCP server
├── transports/        # Transport implementations
│   ├── stdio_transport.py
│   └── http_transport.py
├── tools/            # MCP tool implementations
│   ├── network_tools.py
│   ├── code_tools.py
│   ├── threat_tools.py
│   └── web_tools.py
└── config/           # Server configurations
```

## 🚀 Features

- ✅ **Dual Transport**: Stdio (local) and HTTP/SSE (remote)
- ✅ **8+ Security Tools**: Network, code, threat intelligence, web
- ✅ **API Key Authentication**: Secure remote access
- ✅ **Rate Limiting**: Prevent abuse
- ✅ **Access Control**: Network-based restrictions
- ✅ **Audit Logging**: Track all tool executions

## 🔧 Usage

### Local (Stdio Transport)

For use with Claude Desktop or other local MCP clients.

```bash
python -m mcp-server.server --transport stdio
```

**Claude Desktop Configuration:**
```json
{
  "mcpServers": {
    "sec-llama": {
      "command": "python",
      "args": ["-m", "mcp-server.server", "--transport", "stdio"],
      "cwd": "/path/to/Sec-llama"
    }
  }
}
```

### Remote (HTTP/SSE Transport)

For LAN or remote access.

```bash
python -m mcp-server.server \
  --transport http \
  --host 0.0.0.0 \
  --port 8765 \
  --api-keys key1,key2
```

**Client Usage:**
```python
import httpx

headers = {"X-API-Key": "your-api-key"}
response = httpx.post(
    "http://server:8765/sse",
    headers=headers,
    json={"method": "tools/list"}
)
```

## 🛠️ Available Tools

### Network Tools
- `network_discover` - Discover hosts in subnet
- `network_scan` - Port scanning with AI analysis
- `network_vuln_scan` - Vulnerability scanning

### Code Analysis Tools
- `code_scan` - SAST code analysis
- `code_review` - AI-powered code review
- `secret_scan` - Secret detection

### Threat Intelligence Tools
- `threat_cve_lookup` - CVE database lookup
- `threat_ioc_check` - IOC verification
- `threat_apt_info` - APT information

### Web Security Tools
- `web_scan` - OWASP Top 10 scanning
- `web_api_test` - API security testing

## ⚙️ Configuration

Edit `config/mcp_server_config.yaml`:

```yaml
server:
  name: "sec-llama"
  version: "1.0.0"

transport:
  stdio:
    enabled: true
  http:
    enabled: true
    host: "0.0.0.0"
    port: 8765

auth:
  type: "api_key"
  api_keys:
    - name: "admin"
      key: "your-secure-key"
      permissions: ["*"]

security:
  allowed_networks:
    - "192.168.0.0/16"
    - "10.0.0.0/8"
  require_confirmation: true

ollama:
  host: "http://localhost:11434"
  model: "llama3.1:8b"
  timeout: 120
```

## 📊 Monitoring

View server logs:
```bash
tail -f logs/mcp_server.log
```

Check running server:
```bash
curl http://localhost:8765/health
```

## 🐳 Docker Deployment

```bash
# Using Docker Compose
cd deployments/docker
docker-compose -f docker-compose.mcp.yml up -d

# Using Docker Stack
cd deployments/docker-stack
docker stack deploy -c docker-stack.yml sec-llama
```

## 📚 Documentation

- [MCP Server Guide](../docs/MCP_SERVER_GUIDE.md)
- [Tool Documentation](tools/README.md)
- [API Reference](../docs/API_REFERENCE.md)

## 🔒 Security Best Practices

1. **Use strong API keys** (32+ characters)
2. **Restrict network access** to trusted IPs
3. **Enable rate limiting**
4. **Monitor audit logs** regularly
5. **Keep secrets secure** (use Docker secrets in production)
6. **Use HTTPS** in production (via Nginx reverse proxy)

---

**Start the server:**
```bash
python -m mcp-server.server --transport stdio
```

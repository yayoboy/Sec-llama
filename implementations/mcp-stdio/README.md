# MCP stdio - Claude Desktop Integration

Integra Sec-Llama direttamente in Claude Desktop tramite MCP stdio transport.

## 🚀 Quick Start

```bash
# Setup (una volta)
./setup.sh

# Avvia server MCP
./start.sh

# Restart Claude Desktop
# Gli strumenti Sec-Llama appariranno automaticamente!
```

## 📦 Installazione

```bash
./setup.sh
```

Questo configura:
- Virtual environment Python
- Dipendenze MCP
- Collegamenti ai moduli shared
- Configurazione automatica Claude Desktop

## 🎯 Features

### Security Tools in Claude Desktop
- ✅ **Network Scan** - Scansione rete e discovery
- ✅ **Port Scan** - Scansione porte servizi
- ✅ **Code Analysis** - Analisi SAST codice
- ✅ **CVE Lookup** - Ricerca vulnerabilità
- ✅ **IOC Analysis** - Analisi indicatori compromissione
- ✅ **Container Scan** - Scansione container Docker
- ✅ **Exploit Search** - Ricerca exploit disponibili
- ✅ **Payload Generator** - Generazione payload

### Automatic Integration
- ✅ **Zero Configuration** - Setup automatico Claude Desktop
- ✅ **stdio Transport** - Comunicazione locale via stdio
- ✅ **Tool Discovery** - Claude scopre automaticamente gli strumenti
- ✅ **Secure** - Solo accesso locale, nessuna rete

## 🔧 Configurazione

### Configurazione Automatica

Il setup script configura automaticamente Claude Desktop aggiungendo:

**`~/.config/claude/claude_desktop_config.json`:**
```json
{
  "mcpServers": {
    "sec-llama": {
      "command": "/path/to/implementations/mcp-stdio/start.sh"
    }
  }
}
```

### Configurazione Manuale

Se preferisci configurare manualmente:

1. Apri Claude Desktop config:
   ```bash
   nano ~/.config/claude/claude_desktop_config.json
   ```

2. Aggiungi Sec-Llama:
   ```json
   {
     "mcpServers": {
       "sec-llama": {
         "command": "/absolute/path/to/implementations/mcp-stdio/start.sh"
       }
     }
   }
   ```

3. Riavvia Claude Desktop

### Configurare Ollama

Modifica `config.yaml`:
```yaml
ollama:
  host: http://localhost:11434
  model: llama3.1:8b
  timeout: 120
  enabled: true
```

Per Ollama remoto:
```yaml
ollama:
  host: http://192.168.1.100:11434  # IP server Ollama
  model: llama3.1:8b
  timeout: 120
  enabled: true
```

## 🎨 Utilizzo in Claude Desktop

Dopo il setup e il restart di Claude Desktop, puoi usare i tools:

### Esempi

**Network Scanning:**
```
User: "Scan the network 192.168.1.0/24 for active hosts"
Claude: *usa network_scan tool* Here are the active hosts found...
```

**CVE Lookup:**
```
User: "Tell me about CVE-2024-1234"
Claude: *usa cve_lookup tool* This CVE affects...
```

**Code Analysis:**
```
User: "Analyze this Python code for security issues:
def login(username, password):
    query = f'SELECT * FROM users WHERE user=\"{username}\"'
    ..."
Claude: *usa code_analysis tool* I found a SQL injection vulnerability...
```

**Container Security:**
```
User: "Scan the nginx:latest Docker image for vulnerabilities"
Claude: *usa container_scan tool* Found the following vulnerabilities...
```

## 🔍 Tools Disponibili

| Tool | Descrizione | Parametri |
|------|-------------|-----------|
| `network_scan` | Scansione rete | subnet, timeout |
| `port_scan` | Scansione porte | host, ports, scan_type |
| `code_analysis` | Analisi SAST | code, language |
| `cve_lookup` | Ricerca CVE | cve_id |
| `ioc_analysis` | Analisi IOC | indicator |
| `container_scan` | Scan container | image_name |
| `exploit_search` | Ricerca exploit | service, version |
| `payload_generate` | Genera payload | payload_type, target_os |

## 📊 Accesso

- **Transport**: stdio (locale)
- **Configuration**: `~/.config/claude/claude_desktop_config.json`
- **Logs**: `logs/mcp_stdio.log`

## 🆘 Troubleshooting

### Tools non appaiono in Claude Desktop

1. Verifica configurazione:
   ```bash
   cat ~/.config/claude/claude_desktop_config.json
   ```

2. Verifica percorso assoluto:
   ```bash
   which ./start.sh
   pwd
   ```

3. Test manuale:
   ```bash
   ./start.sh
   # Dovrebbe avviarsi senza errori
   ```

4. Restart Claude Desktop completamente (Quit + riavvio)

### Errori di Ollama

Se gli strumenti falliscono con errori Ollama:

```bash
# Verifica Ollama running
curl http://localhost:11434/api/tags

# Avvia Ollama se non running
ollama serve

# Pull model se mancante
ollama pull llama3.1:8b
```

### Logs

Controlla i log per debug:
```bash
tail -f logs/mcp_stdio.log
```

### Permissions

Se hai errori di permessi:
```bash
chmod +x start.sh
chmod +x venv/bin/python
```

## 🔄 Aggiornamento

Per aggiornare Sec-Llama:

```bash
git pull origin main
./setup.sh  # Re-installa dipendenze
# Riavvia Claude Desktop
```

## 🎓 Best Practices

1. **Usa descrizioni chiare** quando chiedi a Claude di usare i tools
2. **Specifica parametri** quando possibile (es. "scan 192.168.1.0/24" invece di "scan the network")
3. **Combina tools** per analisi complesse
4. **Verifica risultati** prima di azioni critiche

## 📚 Esempi Avanzati

### Penetration Testing Workflow

```
User: "I need to assess the security of 192.168.1.50. Can you help?"

Claude: I'll perform a comprehensive security assessment:
1. *network_scan* - Checking if host is up
2. *port_scan* - Finding open ports and services
3. *exploit_search* - Looking for known exploits
4. *payload_generate* - Preparing test payloads

[Detailed results...]
```

### Code Review Workflow

```
User: "Review this authentication code for security issues"
[paste code]

Claude: *code_analysis*
I've identified the following security issues:
1. SQL Injection vulnerability (Critical)
2. Weak password hashing (High)
3. Missing input validation (Medium)
...
```

## 🔗 Links

- **[MCP Protocol](https://modelcontextprotocol.io)** - Model Context Protocol docs
- **[Claude Desktop](https://claude.ai/download)** - Download Claude Desktop
- **[Sec-Llama Main](../../README.md)** - Main documentation

---

**Note:** Questa implementazione usa stdio transport e funziona SOLO in locale con Claude Desktop. Per accesso remoto o via rete, usa [MCP HTTP](../mcp-http/README.md).

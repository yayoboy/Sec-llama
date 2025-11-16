# Standalone - Uso Locale Semplice

Tool da riga di comando per uso locale immediato.

## 🚀 Quick Start

```bash
# 1. Setup
./setup.sh

# 2. Scan network
./sec-llama.sh scan network 192.168.1.0/24

# 3. Analyze code
./sec-llama.sh scan code /path/to/project

# 4. Lookup CVE
./sec-llama.sh threat cve CVE-2021-44228
```

## 📦 Installazione

```bash
./setup.sh
```

Questo installa:
- Python dependencies
- Ollama (opzionale, per AI features)
- Tools di sicurezza necessari

## 💻 Utilizzo

### Network Scanning
```bash
./sec-llama.sh scan network 192.168.1.0/24
./sec-llama.sh scan ports 192.168.1.1
```

### Code Analysis
```bash
./sec-llama.sh scan code /path/to/code
./sec-llama.sh scan secrets /path/to/code
```

### Threat Intelligence
```bash
./sec-llama.sh threat cve CVE-2021-44228
./sec-llama.sh threat ioc 1.2.3.4
```

## ⚙️ Configurazione

Modifica `config.yaml`:

```yaml
ollama:
  host: "http://localhost:11434"
  model: "llama3.1:8b"
  enabled: true  # false per disabilitare AI

output:
  format: "json"  # json, text, html
  directory: "./reports"
```

## 📊 Output

I risultati vengono salvati in `reports/`:
- `reports/network-scan-TIMESTAMP.json`
- `reports/code-analysis-TIMESTAMP.html`
- `reports/threat-intel-TIMESTAMP.txt`

## 🎯 Esempi

### Scan completo di rete
```bash
./sec-llama.sh scan network 192.168.1.0/24 --output reports/network.json
```

### Code review con AI
```bash
./sec-llama.sh scan code ./myproject --ai-review --output reports/code.html
```

### Batch CVE lookup
```bash
./sec-llama.sh threat cve-batch cve-list.txt
```

## 📚 Help

```bash
./sec-llama.sh --help
./sec-llama.sh scan --help
./sec-llama.sh threat --help
```

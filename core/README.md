# Core Security Modules

Core security testing and analysis modules for Sec-Llama.

## 📁 Structure

```
core/
├── network/              # Network security modules
├── code_analysis/        # Code analysis and SAST
├── threat_intel/         # Threat intelligence
├── web_security/         # Web application security
├── exploit/             # Exploitation and pentesting
├── incident_response/   # Incident response automation
├── log_analyzer/        # Log analysis and correlation
├── reporting/           # Report generation
└── container_security/  # Container and K8s security
```

## 🌐 Network Security (`network/`)

Network reconnaissance, scanning, and vulnerability assessment.

**Modules:**
- `discovery/` - Host discovery (ARP, ICMP, TCP)
- `scanning/` - Port scanning (nmap, masscan integration)
- `traffic/` - Traffic analysis and packet inspection
- `wireless/` - WiFi security testing
- `monitoring/` - Network monitoring

**Usage:**
```python
from core.network.discovery import HostDiscovery
from core.network.scanning import PortScanner

# Discover hosts
discovery = HostDiscovery()
hosts = await discovery.discover_subnet("192.168.1.0/24")

# Scan ports
scanner = PortScanner()
results = await scanner.scan(hosts[0], "1-1000")
```

## 💻 Code Analysis (`code_analysis/`)

Static and dynamic code analysis.

**Features:**
- SAST (Static Application Security Testing)
- Dependency vulnerability scanning
- Code quality analysis
- Secret detection
- License compliance

**Tools Integrated:**
- Bandit (Python)
- Semgrep (Multi-language)
- Safety (Dependencies)
- TruffleHog (Secrets)

## 🎯 Threat Intelligence (`threat_intel/`)

Threat intelligence gathering and analysis.

**Features:**
- CVE database lookup
- MITRE ATT&CK mapping
- IOC (Indicators of Compromise) checking
- Threat feed integration
- APT tracking

## 🌍 Web Security (`web_security/`)

Web application security testing.

**Features:**
- OWASP Top 10 testing
- XSS detection
- SQL injection testing
- CSRF validation
- API security testing

## ⚔️ Exploit (`exploit/`)

Exploitation and penetration testing assistance.

**Features:**
- Exploit database search
- Payload generation
- Post-exploitation automation
- Privilege escalation checks
- Lateral movement detection

## 🚨 Incident Response (`incident_response/`)

Automated incident response workflows.

**Features:**
- Alert triage
- Automated investigation
- Evidence collection
- Timeline reconstruction
- Response playbooks

## 📊 Log Analyzer (`log_analyzer/`)

Log analysis and correlation.

**Features:**
- Multi-source log ingestion
- Pattern detection
- Anomaly detection
- Correlation rules
- SIEM integration

## 📄 Reporting (`reporting/`)

Automated report generation.

**Features:**
- PDF/HTML reports
- Executive summaries
- Technical details
- Remediation recommendations
- Customizable templates

## 🐳 Container Security (`container_security/`)

Container and Kubernetes security.

**Features:**
- Image vulnerability scanning
- Container runtime security
- Kubernetes RBAC analysis
- Network policy validation
- Secrets management audit

---

## 🚀 Quick Start

```python
# Import core modules
from core.network.discovery import HostDiscovery
from core.code_analysis import CodeAnalyzer
from core.threat_intel import ThreatIntel

# Network discovery
discovery = HostDiscovery()
hosts = await discovery.discover_subnet("192.168.1.0/24")

# Code analysis
analyzer = CodeAnalyzer()
vulns = await analyzer.scan_directory("/path/to/code")

# Threat intelligence
threat_intel = ThreatIntel()
cve_info = await threat_intel.lookup_cve("CVE-2021-44228")
```

## 📚 Documentation

See individual module README files for detailed documentation:
- [Network Security](network/README.md)
- [Code Analysis](code_analysis/README.md)
- [Threat Intelligence](threat_intel/README.md)

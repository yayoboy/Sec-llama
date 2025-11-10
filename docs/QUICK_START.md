# 🚀 Quick Start Guide

## Installation

### 1. Prerequisites

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.1:8b

# For better results (requires more RAM):
ollama pull llama3.1:70b
```

### 2. Install Sec-Llama Suite

```bash
# Clone repository
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Or use Docker
docker-compose up -d
```

### 3. Initialize Configuration

```bash
# Create config file
sec-llama config --init

# Edit configuration
nano config/config.yaml

# Check dependencies
sec-llama doctor
```

## Basic Usage

### Network Discovery

```bash
# Discover hosts in your network
sec-llama network discover --subnet 192.168.1.0/24

# Use different methods
sec-llama network discover --subnet 192.168.1.0/24 --method icmp
```

### Port Scanning

```bash
# Standard scan
sec-llama network scan --host 192.168.1.10

# Quick scan
sec-llama network scan --host 192.168.1.10 --profile quick

# AI-powered scan strategy
sec-llama network scan --host 192.168.1.10 --ai-suggest

# Scan specific ports
sec-llama network scan --host 192.168.1.10 --ports "22,80,443,3389"
```

### Vulnerability Scanning

```bash
# Network vulnerability scan
sec-llama network vuln-scan --network 192.168.1.0/24

# Code security scan
sec-llama code scan --path ./myapp --language python

# Output to file
sec-llama code scan --path ./myapp --output report.json
```

### Traffic Analysis

```bash
# Analyze PCAP file
sec-llama traffic analyze --pcap capture.pcap

# Capture live traffic
sec-llama traffic capture --interface eth0 --duration 60

# Find credentials in PCAP
sec-llama traffic find-creds --pcap capture.pcap
```

### Wireless Security

```bash
# Scan WiFi networks
sec-llama wireless scan

# Specify interface
sec-llama wireless scan --interface wlan0
```

### Penetration Testing

```bash
# Generate attack plan
sec-llama pentest attack-plan --target 192.168.1.10 --objective "gain root access"

# Find exploits for a service
sec-llama pentest exploit --service Apache --version 2.4.49

# Generate payload
sec-llama pentest payload --type reverse_shell --os linux
```

### Threat Intelligence

```bash
# Lookup CVE
sec-llama threat cve --id CVE-2024-1234

# Search CVEs
sec-llama threat cve-search --keyword "apache" --max 10

# Analyze IOC
sec-llama threat ioc --indicator 192.168.1.100
sec-llama threat ioc --indicator malicious.com
```

### Natural Language Queries

```bash
# Ask questions in plain English
sec-llama ask "Which hosts in my network have RDP exposed?"
sec-llama ask "How do I exploit Apache 2.4.49?"
sec-llama ask "What are the most critical vulnerabilities in my network?"
```

## Common Workflows

### 1. Network Security Assessment

```bash
# Step 1: Discover hosts
sec-llama network discover --subnet 192.168.1.0/24 --output hosts.json

# Step 2: Scan each host
sec-llama network scan --host 192.168.1.10 --ai-suggest --output scan_10.json
sec-llama network scan --host 192.168.1.20 --ai-suggest --output scan_20.json

# Step 3: Full vulnerability assessment
sec-llama network vuln-scan --network 192.168.1.0/24 --depth full
```

### 2. Application Security Testing

```bash
# Scan application code
sec-llama code scan --path /path/to/app --language python --output vulns.json

# Review specific vulnerabilities with AI
sec-llama ask "How serious is the SQL injection found in user_login.py?"
```

### 3. Incident Response

```bash
# Analyze suspicious traffic
sec-llama traffic analyze --pcap suspicious.pcap --ai

# Analyze IOCs
sec-llama threat ioc --indicator 192.168.1.100
sec-llama threat ioc --indicator suspicious-domain.com

# Get AI recommendations
sec-llama ask "I found traffic to 192.168.1.100 on port 4444. What should I do?"
```

### 4. Penetration Test

```bash
# 1. Reconnaissance
sec-llama network discover --subnet 192.168.1.0/24
sec-llama network scan --host 192.168.1.10 --ai-suggest

# 2. Plan attack
sec-llama pentest attack-plan --target 192.168.1.10 --objective "domain admin"

# 3. Find exploits
sec-llama pentest exploit --service "Apache" --version "2.4.49"

# 4. Generate payload
sec-llama pentest payload --type reverse_shell --os linux
```

## Tips & Tricks

### 1. Increase AI Performance

```yaml
# In config/config.yaml
llm:
  model: "llama3.1:70b"  # Use larger model
  temperature: 0.5       # More deterministic
  max_tokens: 8192       # Longer responses
```

### 2. Stealth Mode

```yaml
# In config/config.yaml
network:
  stealth_mode: true
  scan_profiles:
    stealth:
      timing: "T1"  # Slowest, most stealthy
```

### 3. Save Your Scans

```bash
# Always use --output to save results
sec-llama network scan --host 192.168.1.10 --output scan_$(date +%Y%m%d).json
```

### 4. Use Docker for Isolation

```bash
# Run in Docker for isolation
docker-compose run sec-llama network scan --host 192.168.1.10
```

### 5. Batch Processing

```bash
# Scan multiple hosts
for ip in 192.168.1.{1..254}; do
    sec-llama network scan --host $ip --output "scan_$ip.json"
done
```

## Troubleshooting

### Ollama Not Found

```bash
# Check Ollama is running
ollama list

# Start Ollama
systemctl start ollama

# Or run manually
ollama serve
```

### Permission Denied

```bash
# Many tools require root privileges
sudo sec-llama network discover --subnet 192.168.1.0/24

# Or add capabilities
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

### Slow Scans

```bash
# Use faster profile
sec-llama network scan --host 192.168.1.10 --profile quick

# Increase threads in config
network:
  max_threads: 50
```

## Next Steps

- Read the [Complete Guide](guide.md)
- Check [API Documentation](api.md)
- See [Advanced Examples](examples.md)
- Join our [Community](https://github.com/yourusername/Sec-llama/discussions)

## Support

- GitHub Issues: https://github.com/yourusername/Sec-llama/issues
- Discussions: https://github.com/yourusername/Sec-llama/discussions
- Documentation: https://sec-llama.readthedocs.io

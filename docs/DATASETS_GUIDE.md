# 📊 Guida Completa ai Training Dataset

Questa guida spiega **come ottenere e creare** dataset per il training di modelli LLM specializzati in cybersecurity.

---

## 📋 Indice

1. [Panoramica](#panoramica)
2. [Metodo 1: Raccolta Automatica](#metodo-1-raccolta-automatica)
3. [Metodo 2: Dataset Pubblici](#metodo-2-dataset-pubblici)
4. [Metodo 3: Dataset Personalizzati](#metodo-3-dataset-personalizzati)
5. [Metodo 4: Dataset dai Tuoi Tool](#metodo-4-dataset-dai-tuoi-tool)
6. [Preparazione e Validazione](#preparazione-e-validazione)
7. [Best Practices](#best-practices)

---

## 🎯 Panoramica

### Formati Supportati

**Alpaca Format** (Default):
```json
{
  "instruction": "Cosa fare",
  "input": "Contesto o dati",
  "output": "Risposta attesa",
  "metadata": {
    "category": "info opzionali"
  }
}
```

**ShareGPT Format**:
```json
{
  "conversations": [
    {"from": "human", "value": "Domanda"},
    {"from": "gpt", "value": "Risposta"}
  ]
}
```

### Tipi di Dataset

| Tipo | Fonte | Dimensione | Qualità | Difficoltà |
|------|-------|------------|---------|------------|
| CVE Automatici | NVD API | 10K+ items | ⭐⭐⭐⭐ | 🟢 Facile |
| Pubblici | HuggingFace/GitHub | Variabile | ⭐⭐⭐ | 🟢 Facile |
| Template | Pre-popolati | 10-100 items | ⭐⭐⭐ | 🟢 Facile |
| Personalizzati | Creati da te | Custom | ⭐⭐⭐⭐⭐ | 🟡 Media |
| Da Scan Reali | Tue scansioni | Custom | ⭐⭐⭐⭐⭐ | 🟡 Media |

---

## 🤖 Metodo 1: Raccolta Automatica

### A) CVE dal Database NIST

Il metodo **più semplice** per ottenere migliaia di esempi reali:

```bash
# Raccolta automatica da NIST NVD
sec-llama train collect-dataset --type cve --max-items 10000

# Output: database/datasets/cve_dataset_20241113.json
```

**Cosa ottieni:**
- ✅ 10,000 CVE reali con descrizioni
- ✅ CVSS scores e severity levels
- ✅ Metadata (CVE ID, anno, categoria)
- ✅ Formato Alpaca già pronto

**Esempio output:**
```json
{
  "instruction": "Analyze CVE CVE-2024-1234 and provide security assessment",
  "input": "CVE ID: CVE-2024-1234\nDescription: Remote code execution in Apache Struts...",
  "output": "This vulnerability has a CVSS score of 9.8 (CRITICAL). It allows remote attackers to execute arbitrary code...",
  "metadata": {
    "cve_id": "CVE-2024-1234",
    "severity": "CRITICAL",
    "score": 9.8
  }
}
```

**Vantaggi:**
- ⚡ Veloce (5-10 minuti per 10K CVE)
- 📊 Dati reali e aggiornati
- 🎯 Specifico per security
- 🆓 Gratuito (API pubblica NIST)

**Limitazioni:**
- ⚠️ Rate limiting API (6 secondi tra richieste senza API key)
- ⚠️ Solo CVE (no exploit details)

### B) Security Q&A Template

Dataset pre-popolato con concetti security fondamentali:

```bash
# Crea dataset Q&A
sec-llama train collect-dataset --type security-qa

# Output: database/datasets/security_qa_20241113.json
```

**Contiene:**
- SQL Injection, XSS, CSRF
- Privilege Escalation (Linux/Windows)
- Secure Coding best practices
- Network reconnaissance
- ~50+ esempi curati

### C) Exploit Template

```bash
# Dataset exploit comuni
sec-llama train collect-dataset --type exploit

# Output: database/datasets/exploit_dataset_20241113.json
```

---

## 🌐 Metodo 2: Dataset Pubblici

### Script Automatico di Download

```bash
# Script interattivo per scaricare dataset pubblici
./scripts/download_public_datasets.sh
```

**Menu disponibili:**

#### 1. **CyberSecEval** (Meta/Facebook)
- Source: HuggingFace
- Size: ~1000+ esempi
- Content: Security prompts e risposte
- Quality: ⭐⭐⭐⭐⭐

```bash
# Download automatico
./scripts/download_public_datasets.sh
# Seleziona: 1
```

#### 2. **MITRE ATT&CK**
- Source: MITRE CTI GitHub
- Size: 600+ tecniche
- Content: Tattiche e tecniche attacco
- Quality: ⭐⭐⭐⭐⭐

```bash
# Download e conversione automatica
./scripts/download_public_datasets.sh
# Seleziona: 4
```

**Esempio output:**
```json
{
  "instruction": "Explain the Spearphishing Attachment ATT&CK technique",
  "input": "What is T1193 in the MITRE ATT&CK framework?",
  "output": "Spearphishing attachment is a technique where adversaries send targeted emails with malicious attachments...",
  "metadata": {
    "mitre_id": "T1193",
    "tactic": "initial-access"
  }
}
```

#### 3. **ExploitDB Dataset**
- Source: Exploit-DB CSV
- Size: 50,000+ exploits
- Content: Exploit descriptions, platforms, tipi
- Quality: ⭐⭐⭐⭐

```bash
./scripts/download_public_datasets.sh
# Seleziona: 5
```

#### 4. **OWASP Top 10**
- Source: Curato manualmente
- Size: 10 esempi (uno per categoria)
- Content: OWASP Top 10 2021 completo
- Quality: ⭐⭐⭐⭐⭐

```bash
./scripts/download_public_datasets.sh
# Seleziona: 7
```

### Dataset HuggingFace Raccomandati

```bash
# Installa huggingface CLI
pip install huggingface_hub

# Download dataset security
huggingface-cli download facebook/CyberSecEval
huggingface-cli download gretelai/synthetic_text_to_sql
```

---

## 🎨 Metodo 3: Dataset Personalizzati

### Usa Template Fornito

```bash
# Copia template
cp templates/custom_dataset_template.json my_dataset.json

# Modifica con il tuo editor
nano my_dataset.json
```

**Template include:**
- Analisi vulnerabilità codice
- Exploit suggestions
- IOC identification
- Privilege escalation
- Incident response
- Threat hunting

### Crea da Zero

**Esempio: Dataset Pentesting**

```json
[
  {
    "instruction": "Pianifica penetration test per web application",
    "input": "Target: https://example.com\nTechnology: PHP + MySQL\nScope: Black box testing",
    "output": "Piano di penetration test:\n\n1. Reconnaissance:\n   - Enumerazione DNS: dig, nslookup\n   - Port scan: nmap -sV -sC example.com\n   - Web tech fingerprinting: whatweb, wappalyzer\n\n2. Vulnerability Scanning:\n   - SQL injection: sqlmap\n   - XSS: XSStrike\n   - Directory enumeration: gobuster, dirb\n\n3. Exploitation:\n   - Tentativo SQL injection su form login\n   - Test XSS su input fields\n   - File upload vulnerabilities\n\n4. Post-Exploitation:\n   - Privilege escalation se shell ottenuta\n   - Lateral movement\n   - Data exfiltration simulation\n\n5. Reporting:\n   - Documentare tutti i finding\n   - CVSS scoring\n   - Remediation suggestions",
    "metadata": {
      "category": "penetration_testing",
      "phase": "planning",
      "difficulty": "intermediate"
    }
  },
  {
    "instruction": "Analizza header HTTP per security issues",
    "input": "HTTP/1.1 200 OK\nServer: Apache/2.4.41\nX-Powered-By: PHP/7.4.3\nSet-Cookie: session=abc123; path=/",
    "output": "Security issues identificati negli header HTTP:\n\n1. CRITICAL - Missing Security Headers:\n   - X-Content-Type-Options: nosniff (MANCANTE)\n   - X-Frame-Options: DENY (MANCANTE)\n   - Content-Security-Policy (MANCANTE)\n   - Strict-Transport-Security (MANCANTE)\n\n2. HIGH - Information Disclosure:\n   - Server: Apache/2.4.41 (rivela versione esatta)\n   - X-Powered-By: PHP/7.4.3 (rivela tecnologia)\n\n3. MEDIUM - Cookie Insecure:\n   - Cookie senza flag 'Secure'\n   - Cookie senza flag 'HttpOnly'\n   - Cookie senza flag 'SameSite'\n\nRaccomandazioni:\n- Aggiungere tutti gli header di sicurezza\n- Rimuovere header che rivelano versioni\n- Configurare cookie con flag sicuri: Secure; HttpOnly; SameSite=Strict",
    "metadata": {
      "category": "web_security",
      "type": "header_analysis"
    }
  }
]
```

Salva come `database/datasets/my_pentest_dataset.json`

### Script Python per Generare Dataset

```python
# generate_dataset.py
import json
from datetime import datetime

def create_custom_dataset():
    dataset = []

    # Template per diversi tipi di esempi
    categories = {
        "code_analysis": [
            ("Python", "SQL Injection in Flask"),
            ("JavaScript", "XSS in React"),
            ("PHP", "LFI vulnerability"),
        ],
        "network_security": [
            ("Port Scanning", "nmap strategies"),
            ("Traffic Analysis", "Wireshark filters"),
            ("WiFi Security", "WPA2 attacks"),
        ],
        "incident_response": [
            ("Ransomware", "Containment procedures"),
            ("DDoS", "Mitigation strategies"),
            ("Data Breach", "Evidence collection"),
        ]
    }

    for category, items in categories.items():
        for topic, subtopic in items:
            dataset.append({
                "instruction": f"Explain {topic} - {subtopic}",
                "input": f"Provide detailed explanation of {subtopic} in the context of {topic}",
                "output": f"[INSERT YOUR DETAILED EXPLANATION HERE]",
                "metadata": {
                    "category": category,
                    "topic": topic,
                    "created": datetime.now().isoformat()
                }
            })

    # Save dataset
    output_file = f"database/datasets/generated_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"Created {len(dataset)} examples in {output_file}")

if __name__ == "__main__":
    create_custom_dataset()
```

```bash
python3 generate_dataset.py
```

---

## 🔬 Metodo 4: Dataset dai Tuoi Tool

Crea dataset **dalle tue scansioni reali** - il metodo più potente!

### A) Da Risultati Nmap

```python
# scripts/nmap_to_dataset.py
import json
import xml.etree.ElementTree as ET

def nmap_to_dataset(nmap_xml_file):
    tree = ET.parse(nmap_xml_file)
    root = tree.getroot()

    dataset = []

    for host in root.findall('host'):
        ip = host.find('address').get('addr')

        for port in host.findall('.//port'):
            portid = port.get('portid')
            service = port.find('service')

            if service is not None:
                service_name = service.get('name', 'unknown')
                version = service.get('version', '')

                dataset.append({
                    "instruction": f"Analyze service on {ip}:{portid}",
                    "input": f"IP: {ip}\nPort: {portid}\nService: {service_name}\nVersion: {version}",
                    "output": f"Service {service_name} {version} detected on port {portid}. [ADD SECURITY ANALYSIS]",
                    "metadata": {
                        "ip": ip,
                        "port": portid,
                        "service": service_name
                    }
                })

    with open('database/datasets/nmap_results.json', 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"Created {len(dataset)} examples from nmap scan")

# Usage
nmap_to_dataset('scan_results.xml')
```

### B) Da Log di Sicurezza

```python
# scripts/logs_to_dataset.py
import json
import re

def parse_auth_logs(log_file):
    dataset = []

    with open(log_file, 'r') as f:
        for line in f:
            # Detect failed login attempts
            if 'Failed password' in line:
                match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    ip = match.group(1)
                    dataset.append({
                        "instruction": "Analyze authentication failure",
                        "input": f"Log: {line.strip()}",
                        "output": f"Failed login attempt from {ip}. Potential brute-force attack. Recommend: Rate limiting, fail2ban, IP blocking.",
                        "metadata": {
                            "attack_type": "brute_force",
                            "source_ip": ip
                        }
                    })

    with open('database/datasets/auth_logs_dataset.json', 'w') as f:
        json.dump(dataset, f, indent=2)

    return len(dataset)

# Usage
count = parse_auth_logs('/var/log/auth.log')
print(f"Created {count} examples from auth logs")
```

### C) Da Report Burp Suite

```python
# scripts/burp_to_dataset.py
import json
import xml.etree.ElementTree as ET

def burp_to_dataset(burp_xml):
    tree = ET.parse(burp_xml)
    root = tree.getroot()

    dataset = []

    for issue in root.findall('.//issue'):
        name = issue.find('name').text
        severity = issue.find('severity').text
        detail = issue.find('issueDetail').text if issue.find('issueDetail') is not None else ""

        dataset.append({
            "instruction": f"Analyze web vulnerability: {name}",
            "input": f"Vulnerability: {name}\nSeverity: {severity}",
            "output": f"{detail}\n\nSeverity: {severity}\nRemediation: [ADD SPECIFIC REMEDIATION]",
            "metadata": {
                "vulnerability": name,
                "severity": severity,
                "source": "burp_suite"
            }
        })

    with open('database/datasets/burp_findings.json', 'w') as f:
        json.dump(dataset, f, indent=2)

    return len(dataset)
```

---

## ✅ Preparazione e Validazione

### Workflow Completo

```bash
# 1. Raccogli dataset da più fonti
sec-llama train collect-dataset --type cve --max-items 5000
./scripts/download_public_datasets.sh  # Seleziona MITRE + OWASP

# 2. Valida ogni dataset
sec-llama train validate --dataset database/datasets/cve_dataset_20241113.json
sec-llama train validate --dataset database/datasets/mitre_attack.json

# 3. Combina e prepara dataset finale
sec-llama train prepare-data \
  --datasets "database/datasets/cve_dataset_20241113.json,database/datasets/mitre_attack.json,database/datasets/owasp_top10_2021.json" \
  --format alpaca \
  --output final_security_dataset.json

# 4. Verifica statistiche
sec-llama train list-datasets
```

### Validazione Dataset

```bash
# Valida formato e qualità
sec-llama train validate --dataset my_dataset.json
```

**Cosa viene controllato:**
- ✅ Formato JSON valido
- ✅ Campi obbligatori (instruction, output)
- ✅ Lunghezza minima output (>10 caratteri)
- ✅ Campi vuoti
- ✅ Duplicati

### Merge Multiple Dataset

```bash
# Combina più dataset
sec-llama train prepare-data \
  --datasets "dataset1.json,dataset2.json,dataset3.json" \
  --format alpaca \
  --deduplicate \
  --shuffle
```

---

## 📚 Best Practices

### Qualità dei Dataset

**DO:**
- ✅ Usare esempi reali quando possibile
- ✅ Includere metadata per categorizzazione
- ✅ Bilanciare severity levels (LOW/MED/HIGH/CRIT)
- ✅ Variare tipi di vulnerabilità
- ✅ Includere sia offensive che defensive security
- ✅ Usare terminologia tecnica corretta
- ✅ Fornire output dettagliati (200+ caratteri)

**DON'T:**
- ❌ Copiare esempi identici
- ❌ Usare solo un tipo di vulnerabilità
- ❌ Output troppo brevi (<50 caratteri)
- ❌ Informazioni obsolete o incorrette
- ❌ Codice exploit funzionante reale (usare esempi didattici)

### Dimensioni Raccomandate

| Obiettivo | Dimensione Dataset | Tempo Training |
|-----------|-------------------|----------------|
| Proof of Concept | 100-500 esempi | 10-30 min |
| Model Enhancement | 1,000-5,000 esempi | 1-3 ore |
| Specialized Model | 10,000-50,000 esempi | 4-12 ore |
| Production Model | 50,000+ esempi | 12+ ore |

### Bilanciamento Dataset

```python
# Esempio: bilanciare per severity
from collections import Counter
import json

with open('dataset.json', 'r') as f:
    data = json.load(f)

# Count by severity
severities = [item['metadata'].get('severity', 'UNKNOWN') for item in data if 'metadata' in item]
print(Counter(severities))

# Target distribution
# LOW: 20%, MEDIUM: 30%, HIGH: 30%, CRITICAL: 20%
```

### Testing Dataset Quality

Prima del training, testa manualmente alcuni esempi:

```bash
# Testa esempi random con modello base
ollama run llama3.1:8b

# Paste instruction + input dal tuo dataset
# Confronta output del modello con output atteso nel dataset
```

---

## 🔄 Workflow Completo Raccomandato

```bash
# === FASE 1: RACCOLTA ===

# 1a. Dataset automatici (CVE)
sec-llama train collect-dataset --type cve --max-items 10000

# 1b. Dataset pubblici
./scripts/download_public_datasets.sh
# Seleziona: 8 (tutti)

# 1c. Dataset custom (opzionale)
cp templates/custom_dataset_template.json database/datasets/my_custom.json
# Modifica my_custom.json con i tuoi esempi

# === FASE 2: VALIDAZIONE ===

# Valida tutti i dataset
for dataset in database/datasets/*.json; do
    sec-llama train validate --dataset "$dataset"
done

# === FASE 3: PREPARAZIONE ===

# Combina i migliori dataset
sec-llama train prepare-data \
  --datasets "database/datasets/cve_dataset_20241113.json,database/datasets/mitre_attack.json,database/datasets/owasp_top10_2021.json,database/datasets/security_qa_curated.json" \
  --format alpaca \
  --output database/datasets/final_training_data.json

# === FASE 4: TRAINING ===

# Fine-tune model
sec-llama train fine-tune \
  --base-model llama3.1:8b \
  --dataset database/datasets/final_training_data.json \
  --name sec-llama-specialist

# === FASE 5: EVALUATION ===

# Valuta performance
sec-llama train evaluate --model sec-llama-specialist

# Confronta con base model
sec-llama train compare --models "llama3.1:8b,sec-llama-specialist"
```

---

## 📖 Risorse Aggiuntive

### Dataset Pubblici Online

**HuggingFace:**
- `facebook/CyberSecEval` - Meta's security evaluation dataset
- `gretelai/synthetic_text_to_sql` - SQL security examples
- `databricks/databricks-dolly-15k` - General instruction following

**GitHub:**
- [MITRE CTI](https://github.com/mitre/cti) - ATT&CK data
- [ExploitDB](https://gitlab.com/exploit-database/exploitdb) - Exploit database
- [SecLists](https://github.com/danielmiessler/SecLists) - Security lists

**API Gratuite:**
- [NIST NVD](https://nvd.nist.gov/developers/vulnerabilities) - CVE database
- [CVE Details](https://www.cvedetails.com/) - CVE information
- [Exploit-DB API](https://www.exploit-db.com/) - Exploit search

### Tools per Dataset Creation

```bash
# JSON validation
jq . dataset.json > /dev/null && echo "Valid JSON"

# Count examples
jq 'length' dataset.json

# Extract specific fields
jq '.[].instruction' dataset.json

# Filter by metadata
jq '[.[] | select(.metadata.severity == "CRITICAL")]' dataset.json
```

---

## ❓ FAQ

**Q: Quanti esempi servono per un buon modello?**
A: Minimo 1000-5000 esempi di qualità. Per modelli specializzati: 10,000+

**Q: Posso mixare formati Alpaca e ShareGPT?**
A: Sì, lo script `prepare-data` converte automaticamente

**Q: I dataset CVE sono abbastanza?**
A: Per iniziare sì, ma aggiungi dataset su exploit, best practices, e esempi custom per modello più completo

**Q: Posso usare dataset in altre lingue?**
A: Sì, ma performance migliori con dataset nella lingua target del modello

**Q: Come evitare overfitting?**
A: Usa dataset diversificati, validation split, e monitora evaluation metrics

---

**Prossimi Passi:**
1. Raccogli dataset seguendo uno dei metodi
2. Valida qualità con `sec-llama train validate`
3. Leggi [TRAINING.md](TRAINING.md) per iniziare il fine-tuning
4. Consulta [FEATURES.md](FEATURES.md) per funzionalità complete

**Supporto:** Per domande, consulta la documentazione completa o apri una issue su GitHub.

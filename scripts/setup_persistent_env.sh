#!/bin/bash
# Script per configurare Sec-Llama su Kali Live con Persistenza
# Da eseguire DOPO il boot con persistenza abilitata

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Configurazione
INSTALL_DIR="/root/sec-llama"
OLLAMA_MODELS_DIR="/opt/ollama-models"
CONFIG_DIR="$INSTALL_DIR/config"

print_info "Configurazione ambiente persistente per Sec-Llama..."

# 1. Aggiorna sistema (opzionale, commentare se lento)
print_info "Step 1/7: Aggiornamento sistema..."
apt-get update -qq

# 2. Installa dipendenze di sistema
print_info "Step 2/7: Installazione dipendenze di sistema..."
apt-get install -y -qq \
    python3-pip \
    nmap \
    masscan \
    wireshark \
    tshark \
    aircrack-ng \
    tcpdump \
    git \
    curl \
    build-essential \
    libpcap-dev \
    libssl-dev

# 3. Installa Ollama
print_info "Step 3/7: Installazione Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
else
    print_info "Ollama già installato"
fi

# Configura Ollama per usare directory persistente
export OLLAMA_MODELS="$OLLAMA_MODELS_DIR"
echo "export OLLAMA_MODELS=$OLLAMA_MODELS_DIR" >> /root/.bashrc

# Avvia Ollama in background
print_info "Avvio servizio Ollama..."
systemctl start ollama 2>/dev/null || nohup ollama serve > /tmp/ollama.log 2>&1 &
sleep 3

# 4. Clone/Update Sec-Llama
print_info "Step 4/7: Setup Sec-Llama..."
if [ ! -d "$INSTALL_DIR" ]; then
    git clone https://github.com/yourusername/Sec-llama.git "$INSTALL_DIR"
else
    print_info "Sec-Llama già presente, aggiornamento..."
    cd "$INSTALL_DIR"
    git pull
fi

cd "$INSTALL_DIR"

# 5. Installa dipendenze Python (con cache per velocizzare)
print_info "Step 5/7: Installazione dipendenze Python..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# 6. Configura Sec-Llama per ambiente persistente
print_info "Step 6/7: Configurazione Sec-Llama..."

if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    cp "$CONFIG_DIR/config.example.yaml" "$CONFIG_DIR/config.yaml"

    # Ottimizzazioni per live USB
    cat > "$CONFIG_DIR/config.yaml" << 'EOF'
# Sec-Llama Configuration - Optimized for Live USB Persistence

llm:
  provider: "ollama"
  model: "llama3.1:8b-instruct-q4_K_M"  # Modello quantizzato leggero
  base_url: "http://localhost:11434"
  temperature: 0.7
  max_tokens: 2048  # Ridotto per performance
  timeout: 60

rag:
  enabled: false  # Disabilitato per risparmiare RAM

network:
  default_timeout: 20
  max_threads: 4  # Ridotto per USB
  stealth_mode: false
  interface: "eth0"

  scan_profiles:
    live_quick:
      ports: "21,22,23,80,443,3389,8080,8443"
      timing: "T4"
    live_standard:
      ports: "1-1000"
      timing: "T3"

scanning:
  nmap:
    path: "/usr/bin/nmap"
    default_args: "-sV --open"
  masscan:
    path: "/usr/bin/masscan"
    rate: 500  # Ridotto per stabilità

wireless:
  interface: "wlan0"
  monitor_mode: true
  aircrack_path: "/usr/bin/aircrack-ng"

traffic:
  wireshark_path: "/usr/bin/tshark"
  max_packets: 5000  # Ridotto per RAM

code_security:
  languages:
    - python
    - javascript
  bandit:
    enabled: true
    severity: ["HIGH", "CRITICAL"]
  semgrep:
    enabled: false  # Disabilitato per velocità

exploitation:
  metasploit:
    enabled: true
    path: "/usr/bin/msfconsole"
  searchsploit:
    enabled: true
    path: "/usr/bin/searchsploit"

threat_intel:
  cve_db_update: false  # Aggiornamento manuale
  sources:
    - "nvd"
    - "exploit-db"

reporting:
  output_dir: "/root/sec-llama/reports"
  format: "html"  # HTML più leggero di PDF
  include_screenshots: false
  executive_summary: true
  severity_threshold: "HIGH"

database:
  type: "sqlite"
  path: "/root/sec-llama/database"

logging:
  level: "INFO"
  file: "/root/sec-llama/logs/sec-llama.log"
  rotation: "5 MB"
  retention: 5

api:
  enabled: false

web:
  enabled: false

agents:
  enabled: true
  max_concurrent: 2  # Ridotto per RAM

  agents:
    recon:
      enabled: true
      model: "llama3.1:8b-instruct-q4_K_M"
    exploit:
      enabled: true
      model: "llama3.1:8b-instruct-q4_K_M"
    defense:
      enabled: false  # Disabilitato per risparmiare RAM

performance:
  cache_enabled: true
  cache_ttl: 1800
  parallel_scans: false  # Disabilitato per stabilità
  max_workers: 2

security:
  require_confirmation: true
  authorized_networks:
    - "192.168.0.0/16"
    - "10.0.0.0/8"
    - "172.16.0.0/12"
  log_all_operations: true

advanced:
  debug_mode: false
  verbose: false
  dry_run: false
EOF

    print_info "Configurazione creata: $CONFIG_DIR/config.yaml"
else
    print_info "Configurazione esistente mantenuta"
fi

# Crea directory necessarie
mkdir -p "$INSTALL_DIR/reports"
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/database"
mkdir -p "$OLLAMA_MODELS_DIR"

# 7. Download modello LLM (piccolo e veloce)
print_info "Step 7/7: Download modello LLM..."
MODEL_NAME="llama3.1:8b-instruct-q4_K_M"

if ollama list | grep -q "$MODEL_NAME"; then
    print_info "Modello $MODEL_NAME già presente"
else
    print_warning "Download $MODEL_NAME (~4.5GB)... Potrebbe richiedere tempo"
    ollama pull "$MODEL_NAME"
fi

# Aggiungi alias utili
print_info "Aggiunta alias shell..."
cat >> /root/.bashrc << 'EOF'

# Sec-Llama Aliases
alias sec-llama='python3 /root/sec-llama/cli/main.py'
alias sec-scan='sec-llama network discover'
alias sec-report='sec-llama report generate'

# Ollama
export OLLAMA_MODELS=/opt/ollama-models

# Auto-start Ollama
if ! pgrep -x "ollama" > /dev/null; then
    nohup ollama serve > /tmp/ollama.log 2>&1 &
fi
EOF

# Rendi eseguibile il CLI
chmod +x "$INSTALL_DIR/cli/main.py"

# Crea link simbolico
ln -sf "$INSTALL_DIR/cli/main.py" /usr/local/bin/sec-llama

print_info ""
print_info "✓ Setup completato con successo!"
print_info ""
print_info "Componenti installati:"
print_info "  ✓ Ollama con modello $MODEL_NAME"
print_info "  ✓ Sec-Llama in $INSTALL_DIR"
print_info "  ✓ Tool di sicurezza (nmap, masscan, wireshark, aircrack-ng)"
print_info ""
print_info "Directory persistenti:"
print_info "  - Modelli LLM: $OLLAMA_MODELS_DIR"
print_info "  - Reports: $INSTALL_DIR/reports"
print_info "  - Database: $INSTALL_DIR/database"
print_info "  - Logs: $INSTALL_DIR/logs"
print_info ""
print_info "Comandi rapidi:"
print_info "  sec-llama --help           # Help generale"
print_info "  sec-scan 192.168.1.0/24    # Scansione rete"
print_info "  sec-llama pentest plan --target example.com"
print_info ""
print_info "Riavvia il terminale o esegui: source /root/.bashrc"

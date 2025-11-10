#!/bin/bash
# Sec-Llama Suite - Installation Script

set -e

echo "=========================================="
echo "🛡️  Sec-Llama Suite Installer"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Some features require root privileges."
    echo "Consider running with sudo for full functionality."
    echo ""
fi

# Check Python version
echo "[*] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION found"

# Check Ollama
echo ""
echo "[*] Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found."
    read -p "Install Ollama? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "[*] Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        echo "✓ Ollama installed"
    fi
else
    echo "✓ Ollama found"
fi

# Install system dependencies
echo ""
echo "[*] Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y \
        nmap \
        tcpdump \
        wireless-tools \
        aircrack-ng \
        net-tools \
        iputils-ping \
        git \
        || echo "⚠️  Some packages failed to install"
elif command -v yum &> /dev/null; then
    # RedHat/CentOS
    sudo yum install -y \
        nmap \
        tcpdump \
        wireless-tools \
        aircrack-ng \
        net-tools \
        iputils \
        git \
        || echo "⚠️  Some packages failed to install"
elif command -v brew &> /dev/null; then
    # macOS
    brew install nmap tcpdump aircrack-ng || echo "⚠️  Some packages failed to install"
fi

echo "✓ System dependencies installed"

# Create virtual environment
echo ""
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo ""
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo "✓ Python dependencies installed"

# Initialize configuration
echo ""
echo "[*] Initializing configuration..."
mkdir -p config reports logs database

if [ ! -f "config/config.yaml" ]; then
    cp config/config.example.yaml config/config.yaml
    echo "✓ Configuration file created: config/config.yaml"
else
    echo "✓ Configuration file already exists"
fi

# Pull default Ollama model
echo ""
read -p "Pull default LLM model (llama3.1:8b)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[*] Pulling llama3.1:8b model (this may take a while)..."
    ollama pull llama3.1:8b
    echo "✓ Model downloaded"
fi

# Test installation
echo ""
echo "[*] Testing installation..."
sec-llama version
sec-llama doctor

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Edit config: nano config/config.yaml"
echo "  3. Check dependencies: sec-llama doctor"
echo "  4. Run help: sec-llama --help"
echo ""
echo "Examples:"
echo "  sec-llama network discover --subnet 192.168.1.0/24"
echo "  sec-llama network scan --host 192.168.1.1"
echo "  sec-llama code scan --path ./myapp"
echo ""
echo "Documentation: docs/QUICK_START.md"
echo ""

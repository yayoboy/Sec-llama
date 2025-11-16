#!/bin/bash
# Standalone Implementation - Setup Script

set -e

echo "🚀 Sec-Llama Standalone - Setup"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create directories
mkdir -p reports logs database

# Copy default config
if [ ! -f "config.yaml" ]; then
    cp config.example.yaml config.yaml
    echo "⚙️ Created config.yaml (edit as needed)"
fi

# Optional: Install Ollama
read -p "Install Ollama for AI features? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull llama3.1:8b
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  ./sec-llama.sh scan network 192.168.1.0/24"
echo "  ./sec-llama.sh scan code /path/to/code"
echo "  ./sec-llama.sh threat cve CVE-2021-44228"
echo ""

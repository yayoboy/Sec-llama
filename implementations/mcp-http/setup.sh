#!/bin/bash
# MCP HTTP - Setup Script

set -e

echo "🌐 Sec-Llama MCP HTTP - Setup"
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

# Link shared libraries
echo "📦 Linking shared libraries..."
ln -sf ../../shared ./shared

# Create directories
mkdir -p logs config

# Copy default config
if [ ! -f "config.yaml" ]; then
    cp config.example.yaml config.yaml
    echo "⚙️ Created config.yaml (edit as needed)"
fi

# Generate API key
echo ""
echo "🔑 Generating API key..."
API_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 API KEY (save this!):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$API_KEY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Save to .env
cat > .env << EOF
# MCP HTTP Server Configuration
MCP_API_KEYS=$API_KEY
MCP_PORT=8765
OLLAMA_HOST=http://localhost:11434
LOG_LEVEL=INFO
EOF

echo "✅ API key saved to .env"
echo ""

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
echo "  source .env"
echo "  ./start.sh"
echo ""
echo "Or:"
echo "  MCP_API_KEYS=\"$API_KEY\" ./start.sh"
echo ""
echo "Access: http://localhost:8765"
echo ""

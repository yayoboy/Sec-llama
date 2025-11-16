#!/bin/bash
# MCP stdio - Setup Script

set -e

echo "🔌 Sec-Llama MCP stdio - Setup"
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

# Configure Claude Desktop
echo ""
echo "🔧 Configuring Claude Desktop..."

CLAUDE_CONFIG="$HOME/.config/claude/claude_desktop_config.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_SCRIPT="$SCRIPT_DIR/start.sh"

# Make start.sh executable
chmod +x start.sh

# Create Claude config directory
mkdir -p "$HOME/.config/claude"

# Check if config exists
if [ -f "$CLAUDE_CONFIG" ]; then
    echo "⚠️ Claude Desktop config already exists"
    echo "📝 Add this to your config manually:"
    echo ""
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"sec-llama\": {"
    echo "      \"command\": \"$START_SCRIPT\""
    echo "    }"
    echo "  }"
    echo "}"
    echo ""
else
    # Create new config
    cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "sec-llama": {
      "command": "$START_SCRIPT"
    }
  }
}
EOF
    echo "✅ Claude Desktop configured automatically"
fi

# Optional: Install Ollama
echo ""
read -p "Install Ollama for AI features? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull llama3.1:8b
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Ensure Ollama is running: ollama serve"
echo "2. Restart Claude Desktop"
echo "3. Sec-Llama tools will appear automatically!"
echo ""
echo "Configuration: $CLAUDE_CONFIG"
echo "Start script: $START_SCRIPT"
echo ""

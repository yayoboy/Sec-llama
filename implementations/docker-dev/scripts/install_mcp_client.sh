#!/bin/bash
# Configure Claude Desktop to use Sec-Llama MCP Server
# Works on macOS and Linux

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

print_header "Sec-Llama MCP Client Setup"

# Detect OS and set Claude Desktop config path
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    CLAUDE_CONFIG_DIR="$HOME/.config/claude"
    OS="Linux"
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "This script supports macOS and Linux only"
    exit 1
fi

print_info "Detected OS: $OS"
print_info "Claude config directory: $CLAUDE_CONFIG_DIR"

# Create config directory if it doesn't exist
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    print_warning "Claude config directory not found. Creating..."
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Backup existing config
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    BACKUP_FILE="${CLAUDE_CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    print_info "Backing up existing config to: $BACKUP_FILE"
    cp "$CLAUDE_CONFIG_FILE" "$BACKUP_FILE"
fi

# Create MCP server configuration
print_info "Configuring Sec-Llama MCP server..."

# Check if config file exists and has content
if [ -f "$CLAUDE_CONFIG_FILE" ] && [ -s "$CLAUDE_CONFIG_FILE" ]; then
    # File exists and is not empty - merge configuration
    print_info "Merging with existing configuration..."

    # Use Python to merge JSON
    python3 << EOF
import json
import sys

config_file = "$CLAUDE_CONFIG_FILE"
project_root = "$PROJECT_ROOT"

# Read existing config
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {}

# Ensure mcpServers exists
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# Add Sec-Llama server
config['mcpServers']['sec-llama'] = {
    "command": "python3",
    "args": [
        f"{project_root}/mcp_server/server.py",
        "--transport",
        "stdio"
    ],
    "env": {
        "PYTHONPATH": project_root,
        "OLLAMA_HOST": "http://localhost:11434"
    }
}

# Write updated config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration updated: {config_file}")
EOF

else
    # Create new config file
    print_info "Creating new configuration file..."

    cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "sec-llama": {
      "command": "python3",
      "args": [
        "$PROJECT_ROOT/mcp_server/server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_ROOT",
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  }
}
EOF

    print_info "✓ Configuration file created: $CLAUDE_CONFIG_FILE"
fi

# Display configuration
print_header "Configuration Complete"
echo ""
echo "Claude Desktop is now configured to use Sec-Llama MCP server!"
echo ""
echo "Configuration file: $CLAUDE_CONFIG_FILE"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Ensure Ollama is running:"
echo "   $ ollama serve"
echo ""
echo "2. Pull required model (if not already done):"
echo "   $ ollama pull llama3.1:8b"
echo ""
echo "3. Restart Claude Desktop to load the MCP server"
echo ""
echo "4. In Claude Desktop, you should see 'sec-llama' in available tools"
echo ""
echo "5. Try a command like:"
echo "   'Use network_discover to scan 192.168.1.0/24'"
echo "   'Use threat_cve_lookup to analyze CVE-2021-41773'"
echo "   'Use code_scan to check /path/to/code for vulnerabilities'"
echo ""

# Show current configuration
print_header "Current Configuration"
cat "$CLAUDE_CONFIG_FILE"
echo ""

# Verify Ollama is running
print_header "System Check"

if command -v ollama &> /dev/null; then
    print_info "✓ Ollama installed"

    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_info "✓ Ollama is running"

        # Check if model is available
        if ollama list | grep -q "llama3.1:8b"; then
            print_info "✓ Model llama3.1:8b is available"
        else
            print_warning "Model llama3.1:8b not found"
            echo "  Run: ollama pull llama3.1:8b"
        fi
    else
        print_warning "Ollama is not running"
        echo "  Run: ollama serve"
    fi
else
    print_warning "Ollama not found"
    echo "  Install from: https://ollama.ai/download"
fi

# Check Python
if python3 --version > /dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_info "✓ Python $PYTHON_VERSION installed"
else
    print_warning "Python 3 not found"
fi

echo ""
print_info "Setup complete! Restart Claude Desktop to use Sec-Llama MCP server."

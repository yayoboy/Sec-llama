#!/bin/bash
# MCP HTTP - Start Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parse arguments
GENERATE_KEY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --generate-key)
            GENERATE_KEY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./start.sh [--generate-key]"
            exit 1
            ;;
    esac
done

# Generate API key if requested
if [ "$GENERATE_KEY" = true ]; then
    NEW_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔐 New API KEY:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$NEW_KEY"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Export this key:"
    echo "  export MCP_API_KEYS=\"$NEW_KEY\""
    echo ""
    exit 0
fi

# Load .env if exists
if [ -f .env ]; then
    echo "📦 Loading environment from .env..."
    source .env
fi

# Check API key
if [ -z "$MCP_API_KEYS" ]; then
    echo "⚠️ WARNING: No API key set!"
    echo ""
    echo "Set API key with:"
    echo "  export MCP_API_KEYS=\"your-api-key\""
    echo ""
    echo "Or generate one with:"
    echo "  ./start.sh --generate-key"
    echo ""
    read -p "Continue without API key? (NOT RECOMMENDED) (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate venv
source venv/bin/activate

# Default port
PORT=${MCP_PORT:-8765}

echo ""
echo "🚀 Starting MCP HTTP Server..."
echo ""
echo "Access: http://localhost:$PORT"
echo "Health: http://localhost:$PORT/health"
echo ""

# Run MCP HTTP server
python -m mcp_server.http_transport --host 0.0.0.0 --port "$PORT"

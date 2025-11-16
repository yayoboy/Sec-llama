#!/bin/bash
# Start Sec-Llama MCP Server
# Usage: ./start_mcp_server.sh [stdio|http]

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Transport mode (default: stdio)
MODE="${1:-stdio}"

# Change to project root
cd "$PROJECT_ROOT"

print_header "Sec-Llama MCP Server"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if MCP dependencies are installed
if ! python3 -c "import mcp" 2>/dev/null; then
    print_warning "MCP dependencies not installed. Installing..."
    pip install -r requirements-mcp.txt
fi

# Start server based on mode
case $MODE in
    stdio)
        print_info "Starting MCP server in stdio mode (local use)..."
        print_info "For Claude Desktop, add this to your config:"
        echo ""
        echo "{
  \"mcpServers\": {
    \"sec-llama\": {
      \"command\": \"python3\",
      \"args\": [\"$PROJECT_ROOT/mcp_server/server.py\", \"--transport\", \"stdio\"],
      \"env\": {
        \"PYTHONPATH\": \"$PROJECT_ROOT\"
      }
    }
  }
}"
        echo ""
        print_info "Starting server..."
        python3 mcp_server/server.py --transport stdio
        ;;

    http)
        print_info "Starting MCP server in HTTP mode (LAN use)..."

        # Get configuration
        HOST="${MCP_HOST:-0.0.0.0}"
        PORT="${MCP_PORT:-8765}"

        # API Keys
        if [ -z "$MCP_API_KEYS" ]; then
            print_warning "No API keys configured (authentication disabled)"
            print_warning "Set MCP_API_KEYS environment variable for production use"
            echo "Example: export MCP_API_KEYS='key1,key2,key3'"
        else
            NUM_KEYS=$(echo "$MCP_API_KEYS" | tr ',' '\n' | wc -l)
            print_info "Loaded $NUM_KEYS API key(s)"
        fi

        print_info "Configuration:"
        print_info "  Host: $HOST"
        print_info "  Port: $PORT"
        print_info "  SSE Endpoint: http://$HOST:$PORT/sse"
        print_info "  Health Check: http://$HOST:$PORT/health"
        print_info "  Tools List: http://$HOST:$PORT/tools"

        # Start server
        if [ -n "$MCP_API_KEYS" ]; then
            python3 mcp_server/server.py \
                --transport http \
                --host "$HOST" \
                --port "$PORT" \
                --api-keys "$MCP_API_KEYS"
        else
            python3 mcp_server/server.py \
                --transport http \
                --host "$HOST" \
                --port "$PORT"
        fi
        ;;

    *)
        echo "Usage: $0 {stdio|http}"
        echo ""
        echo "Modes:"
        echo "  stdio - Local communication (for Claude Desktop)"
        echo "  http  - HTTP/SSE server (for LAN access)"
        echo ""
        echo "Environment variables for HTTP mode:"
        echo "  MCP_HOST      - Host to bind (default: 0.0.0.0)"
        echo "  MCP_PORT      - Port to listen (default: 8765)"
        echo "  MCP_API_KEYS  - Comma-separated API keys (optional)"
        echo ""
        echo "Examples:"
        echo "  $0 stdio                     # Local mode"
        echo "  $0 http                      # HTTP mode, no auth"
        echo "  MCP_API_KEYS='abc123' $0 http  # HTTP with auth"
        exit 1
        ;;
esac

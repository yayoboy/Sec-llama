#!/bin/bash
# MCP HTTP - Unified Start Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║         Sec-Llama MCP HTTP                           ║
║         Remote MCP Server + Web UI                   ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check for --generate-key flag
if [[ "$1" == "--generate-key" ]]; then
    NEW_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔐 New API KEY:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$NEW_KEY"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Add to .env:"
    echo "  MCP_API_KEYS=$NEW_KEY"
    exit 0
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Run ./setup.sh first${NC}"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Load .env if exists
if [ -f .env ]; then
    source .env
fi

# Menu selection
echo -e "${GREEN}Select mode:${NC}"
echo "1) MCP Server - HTTP/SSE API (port 8765)"
echo "2) Web UI - Web interface (port 8080)"
echo "3) Both - MCP Server + Web UI"
echo "4) Docker - Start with Docker Compose"
echo ""
read -p "Choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}Starting MCP HTTP Server...${NC}"
        echo ""

        # Check API key
        if [ -z "$MCP_API_KEYS" ]; then
            echo -e "${YELLOW}⚠️ No API key set!${NC}"
            echo "Generate one with: ./start.sh --generate-key"
            echo ""
            read -p "Continue without API key? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi

        PORT=${MCP_PORT:-8765}
        echo "MCP Server: http://localhost:$PORT"
        echo "Health: http://localhost:$PORT/health"
        echo ""

        python -m mcp_server.transports.http_transport --host 0.0.0.0 --port "$PORT"
        ;;

    2)
        echo -e "${BLUE}Starting Web UI...${NC}"
        echo ""

        echo "Web UI: http://localhost:8080"
        echo "Press Ctrl+C to stop"
        echo ""

        python -m uvicorn web_ui.backend.main:app --host 0.0.0.0 --port 8080
        ;;

    3)
        echo -e "${BLUE}Starting MCP Server + Web UI...${NC}"
        echo ""

        # Check API key
        if [ -z "$MCP_API_KEYS" ]; then
            echo -e "${YELLOW}⚠️ No API key set for MCP server${NC}"
        fi

        PORT=${MCP_PORT:-8765}

        # Start MCP server in background
        python -m mcp_server.transports.http_transport --host 0.0.0.0 --port "$PORT" &
        MCP_PID=$!

        # Start Web UI in background
        python -m uvicorn web_ui.backend.main:app --host 0.0.0.0 --port 8080 &
        WEB_PID=$!

        echo ""
        echo -e "${GREEN}Services started!${NC}"
        echo "  MCP Server: http://localhost:$PORT (PID: $MCP_PID)"
        echo "  Web UI: http://localhost:8080 (PID: $WEB_PID)"
        echo ""
        echo "Press Ctrl+C to stop both"

        # Wait and handle Ctrl+C
        trap "kill $MCP_PID $WEB_PID 2>/dev/null; exit" INT
        wait
        ;;

    4)
        echo -e "${BLUE}Starting with Docker Compose...${NC}"
        echo ""

        if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
            echo -e "${YELLOW}Docker Compose not found${NC}"
            exit 1
        fi

        if [ ! -f ".env" ]; then
            echo "Creating .env..."
            cp .env.example .env
            # Generate API key
            API_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
            sed -i "s/generate-secure-key-here/$API_KEY/g" .env 2>/dev/null || \
                sed -i '' "s/generate-secure-key-here/$API_KEY/g" .env
            echo -e "${GREEN}Generated secure API key in .env${NC}"
        fi

        docker-compose up -d

        echo ""
        echo -e "${GREEN}Services started!${NC}"
        echo ""
        echo "Access:"
        echo "  MCP Server: http://localhost:8765"
        echo "  Ollama: http://localhost:11434"
        echo ""
        echo "Pull model:"
        echo "  docker-compose exec ollama ollama pull llama3.1:8b"
        echo ""
        echo "Logs:"
        echo "  docker-compose logs -f"
        echo ""
        echo "Stop:"
        echo "  docker-compose down"
        ;;

    *)
        echo -e "${YELLOW}Invalid choice${NC}"
        exit 1
        ;;
esac

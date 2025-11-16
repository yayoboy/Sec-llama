#!/bin/bash
# Sec-Llama Standalone - Unified Start Script

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
║         Sec-Llama Standalone                         ║
║         Local LLM Security Suite                     ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Run ./setup.sh first${NC}"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Menu selection
echo -e "${GREEN}Select mode:${NC}"
echo "1) CLI Mode - Command line tools"
echo "2) Web UI - Web interface (port 8080)"
echo "3) Both - CLI + Web UI"
echo "4) Docker - Start with Docker Compose"
echo ""
read -p "Choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}Starting CLI mode...${NC}"
        echo ""
        echo "Usage:"
        echo "  python -m cli.main scan network 192.168.1.0/24"
        echo "  python -m cli.main threat cve CVE-2024-1234"
        echo "  python -m cli.main --help"
        echo ""
        python -m cli.main "$@"
        ;;

    2)
        echo -e "${BLUE}Starting Web UI...${NC}"
        echo ""
        # Check if Ollama is running
        if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${YELLOW}Warning: Ollama not detected on localhost:11434${NC}"
            echo "Start Ollama with: ollama serve"
            echo ""
        fi

        echo "Web UI will start on: http://localhost:8080"
        echo "Press Ctrl+C to stop"
        echo ""
        python -m uvicorn web_ui.backend.main:app --host 0.0.0.0 --port 8080
        ;;

    3)
        echo -e "${BLUE}Starting CLI + Web UI...${NC}"
        echo ""
        echo "Web UI: http://localhost:8080"
        echo "CLI: Available in this terminal"
        echo ""

        # Start Web UI in background
        python -m uvicorn web_ui.backend.main:app --host 0.0.0.0 --port 8080 &
        WEB_PID=$!

        echo "Web UI started (PID: $WEB_PID)"
        echo ""
        echo "You can now use CLI commands:"
        echo "  python -m cli.main scan network 192.168.1.0/24"
        echo ""
        echo "Press Ctrl+C to stop both"

        # Wait for Ctrl+C
        trap "kill $WEB_PID 2>/dev/null; exit" INT
        wait $WEB_PID
        ;;

    4)
        echo -e "${BLUE}Starting with Docker Compose...${NC}"
        echo ""

        if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
            echo -e "${YELLOW}Docker not found. Install Docker first.${NC}"
            exit 1
        fi

        if [ ! -f ".env" ]; then
            echo "Creating .env from example..."
            cp .env.example .env
            echo -e "${YELLOW}Please edit .env with secure passwords${NC}"
            read -p "Press Enter to continue..."
        fi

        docker-compose up -d
        echo ""
        echo -e "${GREEN}Services started!${NC}"
        echo ""
        echo "Access:"
        echo "  Web UI: http://localhost:8080"
        echo "  Ollama: http://localhost:11434"
        echo ""
        echo "Pull Ollama model:"
        echo "  docker-compose exec ollama ollama pull llama3.1:8b"
        echo ""
        echo "View logs:"
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

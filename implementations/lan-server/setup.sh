#!/bin/bash
# ============================================================================
# Sec-Llama LAN Server - Setup Script
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║         Sec-Llama LAN Server - Setup                 ║
║         Security Suite with Remote LLM               ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check Python version
echo -e "${BLUE}[1/7] Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "${BLUE}[2/7] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}[3/7] Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install Python dependencies
echo -e "${BLUE}[4/7] Installing Python dependencies...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Create .env file
echo -e "${BLUE}[5/7] Setting up environment configuration...${NC}"
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
    else
        echo -e "${YELLOW}Keeping existing .env file${NC}"
    fi
else
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created from template${NC}"
fi

# Configure LLM
echo -e "${BLUE}[6/7] Configuring remote LLM...${NC}"
echo ""
echo "Do you have a remote LLM server? (Ollama or LM Studio)"
read -p "Enter choice (ollama/lm-studio/skip): " llm_choice

case $llm_choice in
    ollama)
        read -p "Enter Ollama server IP:PORT (e.g., 192.168.1.100:11434): " ollama_host
        read -p "Enter model name (default: llama3.1:8b): " ollama_model
        ollama_model=${ollama_model:-llama3.1:8b}

        # Update .env
        sed -i.bak "s|LLM_PROVIDER=.*|LLM_PROVIDER=ollama|" .env
        sed -i.bak "s|OLLAMA_HOST=.*|OLLAMA_HOST=http://${ollama_host}|" .env
        sed -i.bak "s|OLLAMA_MODEL=.*|OLLAMA_MODEL=${ollama_model}|" .env
        rm .env.bak

        echo -e "${GREEN}✓ Ollama configured: http://${ollama_host} with model ${ollama_model}${NC}"
        ;;
    lm-studio)
        read -p "Enter LM Studio server IP:PORT (e.g., 192.168.1.100:1234): " lm_studio_host
        read -p "Enter model name: " lm_studio_model

        # Update .env
        sed -i.bak "s|LLM_PROVIDER=.*|LLM_PROVIDER=lm-studio|" .env
        sed -i.bak "s|LM_STUDIO_HOST=.*|LM_STUDIO_HOST=http://${lm_studio_host}|" .env
        sed -i.bak "s|LM_STUDIO_MODEL=.*|LM_STUDIO_MODEL=${lm_studio_model}|" .env
        rm .env.bak

        echo -e "${GREEN}✓ LM Studio configured: http://${lm_studio_host}${NC}"
        ;;
    *)
        echo -e "${YELLOW}⚠ Skipping LLM configuration${NC}"
        echo -e "${YELLOW}You can configure it later by editing .env file${NC}"
        ;;
esac

# Create necessary directories
echo -e "${BLUE}[7/7] Creating necessary directories...${NC}"
mkdir -p logs reports database static
echo -e "${GREEN}✓ Directories created${NC}"

# Setup complete
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                       ║${NC}"
echo -e "${GREEN}║              Setup completed successfully!            ║${NC}"
echo -e "${GREEN}║                                                       ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo -e "1. ${YELLOW}Edit .env file${NC} and update:"
echo "   - SECRET_KEY (generate a secure random string)"
echo "   - JWT_SECRET_KEY (generate a secure random string)"
echo "   - POSTGRES_PASSWORD (for Docker deployment)"
echo "   - REDIS_PASSWORD (for Docker deployment)"
echo ""
echo -e "2. ${YELLOW}Start the application:${NC}"
echo "   ${GREEN}# Local development:${NC}"
echo "   source venv/bin/activate"
echo "   uvicorn web_ui.backend.main:app --host 0.0.0.0 --port 8080 --reload"
echo ""
echo "   ${GREEN}# With Docker Compose:${NC}"
echo "   docker-compose up -d"
echo ""
echo "   ${GREEN}# With Portainer:${NC}"
echo "   - Upload portainer-stack.yml to Portainer"
echo "   - Add environment variables from portainer-env.txt"
echo "   - Deploy the stack"
echo ""
echo -e "3. ${YELLOW}Access the Web UI:${NC}"
echo "   http://localhost:8080"
echo ""
echo -e "${BLUE}Documentation:${NC} See README.md for detailed instructions"
echo ""

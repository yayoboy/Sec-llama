#!/bin/bash

# Sec-Llama Web UI Build Script
# Builds the Vue.js frontend for production

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Building Sec-Llama Web UI ===${NC}"
echo ""

# Check if Node.js is available
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm not found. Please install Node.js${NC}"
    exit 1
fi

# Navigate to frontend directory
cd "$PROJECT_ROOT/web_ui/frontend"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
npm install

# Build frontend
echo -e "${YELLOW}Building frontend...${NC}"
npm run build

# Verify build
if [ -d "../backend/static" ]; then
    echo -e "${GREEN}✓ Frontend built successfully${NC}"
    echo -e "${GREEN}✓ Static files copied to backend/static/${NC}"
    echo ""
    echo "Build complete! You can now start the Web UI with:"
    echo "  ./scripts/start_web_ui.sh --mode production"
else
    echo -e "${RED}✗ Build failed - static directory not found${NC}"
    exit 1
fi

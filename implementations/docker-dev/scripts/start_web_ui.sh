#!/bin/bash

# Sec-Llama Web UI Startup Script
# Starts the FastAPI backend and optionally the Vue.js frontend dev server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
MODE="production"
BACKEND_PORT=8080
FRONTEND_PORT=3000
BACKEND_ONLY=false

# Help function
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Start the Sec-Llama Web UI

OPTIONS:
    -m, --mode MODE         Run mode: development|production (default: production)
    -b, --backend-port      Backend port (default: 8080)
    -f, --frontend-port     Frontend dev server port (default: 3000)
    --backend-only          Start only backend (production mode)
    -h, --help              Show this help message

EXAMPLES:
    # Start in production mode (serves built frontend from backend)
    $0 --mode production

    # Start in development mode (separate backend and frontend servers)
    $0 --mode development

    # Start only backend
    $0 --backend-only


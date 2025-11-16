#!/bin/bash
# Web UI Full - Start Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODE="production"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dev|--development)
            MODE="development"
            shift
            ;;
        --prod|--production)
            MODE="production"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Activate venv
source venv/bin/activate

if [ "$MODE" = "development" ]; then
    echo "🚀 Starting in DEVELOPMENT mode..."
    echo "   Backend: http://localhost:8080"
    echo "   Frontend: http://localhost:3000"
    echo ""

    # Start backend in background
    python -m web_ui.backend.main --reload &
    BACKEND_PID=$!

    # Start frontend dev server
    cd frontend
    npm run dev

    # Cleanup
    kill $BACKEND_PID
else
    echo "🚀 Starting in PRODUCTION mode..."
    echo "   Access: http://localhost:8080"
    echo ""

    # Start backend (serves built frontend)
    python -m web_ui.backend.main
fi

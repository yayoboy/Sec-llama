#!/bin/bash
# MCP stdio - Start Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv
source venv/bin/activate

# Run MCP stdio server
python -m mcp_server.stdio_transport

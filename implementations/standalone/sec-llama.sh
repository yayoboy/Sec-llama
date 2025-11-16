#!/bin/bash
# Sec-Llama Standalone CLI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv
source venv/bin/activate

# Run main CLI
python -m cli.main "$@"

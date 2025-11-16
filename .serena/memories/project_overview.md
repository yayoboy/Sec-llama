# Sec-Llama - Project Overview

## Purpose
Complete cybersecurity testing platform powered by local LLMs. The suite provides AI-enhanced security testing, vulnerability assessment, and penetration testing capabilities - all running 100% locally for privacy.

## Key Features
- **Network Security**: Discovery, port scanning, traffic analysis, wireless auditing
- **Application Security**: SAST (Python, JS, Java, Go, PHP), code review, dependency scanning, container security, API fuzzing
- **Penetration Testing**: Exploit suggestions, payload crafting, attack surface analysis
- **Threat Intelligence**: CVE lookup (NVD API), IOC analysis, OSINT
- **Log Analysis & SIEM**: Multi-format parsing, attack detection, anomaly detection
- **Incident Response**: IR automation, NIST playbooks, containment planning
- **LLM Training**: Dataset collection, model fine-tuning, evaluation
- **Multi-Agent System**: Recon, Exploit, Defense agents with coordinator

## Implementations
7 independent implementations in `implementations/`:
1. **standalone** - CLI tool for local use
2. **mcp-stdio** - MCP server for Claude Desktop integration
3. **mcp-http** - Remote MCP server with HTTP/SSE
4. **web-ui-full** - Complete web interface with AI configuration
5. **docker-dev** - Development environment
6. **docker-production** - Production deployment with Docker Stack
7. **live-usb** - Bootable USB for portable testing

Each implementation is self-contained with its own dependencies, config, and README.

## Project Structure
```
Sec-llama/
├── implementations/        # 7 independent implementations
│   ├── standalone/        # CLI + Web UI
│   ├── mcp-stdio/         # MCP for Claude Desktop
│   ├── mcp-http/          # MCP HTTP server
│   ├── web-ui-full/       # Full web interface
│   ├── docker-dev/        # Dev environment
│   ├── docker-production/ # Production stack
│   └── live-usb/          # Bootable USB
├── docs/                  # Documentation
├── examples/              # Empty (to be populated)
└── README.md              # Main documentation
```

## Common Implementation Structure
Each implementation follows a similar pattern:
```
implementations/[name]/
├── README.md              # Specific docs
├── setup.sh               # Automated setup
├── start.sh               # Unified start script
├── requirements.txt       # Base dependencies
├── requirements-full.txt  # Full dependencies (with Web UI)
├── config/                # Configuration files
├── modules/               # Security modules
│   ├── network/          # Network security
│   ├── threat_intel/     # Threat intelligence
│   ├── code_review/      # Code analysis
│   ├── vuln_scanner/     # Vulnerability scanning
│   ├── container_security/ # Container scanning
│   ├── api_security/     # API fuzzing
│   ├── log_analyzer/     # Log analysis
│   ├── incident_response/ # IR orchestration
│   ├── pentest_assistant/ # Attack planning
│   ├── training/         # LLM training
│   └── reporting/        # Report generation
├── web_ui/               # Web interface (when applicable)
│   ├── backend/          # FastAPI backend
│   └── frontend/         # Vue.js frontend
├── cli/                  # CLI tools (standalone only)
├── mcp-server/           # MCP server code (MCP implementations)
└── database/             # Local database

```

## Important Note: Missing Core Module
Code references `from core.config import get_config`, `from core.llm_interface import get_llm`, etc., but the `core` module doesn't exist in the repository yet. This appears to be a placeholder/TODO that needs implementation.
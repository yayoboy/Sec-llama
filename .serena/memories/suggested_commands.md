# Sec-Llama - Suggested Commands

## Setup Commands

### Initial Setup (any implementation)
```bash
cd implementations/[implementation-name]
./setup.sh
```
The setup script will:
- Create Python virtual environment
- Install dependencies (base + Web UI if applicable)
- Install Node.js dependencies for frontend
- Create default configurations
- Optionally install Ollama and models

### Ollama Installation
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models
ollama pull llama3.1:8b        # Faster, good for most tasks
ollama pull llama3.1:70b       # Better reasoning, slower

# Start Ollama server
ollama serve                    # Default: http://localhost:11434
```

## Running the Application

### Standalone Implementation
```bash
cd implementations/standalone

# Interactive start menu
./start.sh
# Options:
#   1) CLI Mode
#   2) Web UI (http://localhost:8080)
#   3) Both
#   4) Docker

# Direct CLI usage
./sec-llama.sh <command>
# or
python -m cli.main <command>

# Direct Web UI start
python -m uvicorn web_ui.backend.main:app --host 0.0.0.0 --port 8080
```

### MCP HTTP Implementation
```bash
cd implementations/mcp-http
./start.sh
# Options:
#   1) MCP Server only (port 8765)
#   2) Web UI only (port 8080)
#   3) Both
#   4) Docker
```

### MCP STDIO Implementation
```bash
cd implementations/mcp-stdio
./setup.sh    # Auto-configures Claude Desktop
./start.sh
# Restart Claude Desktop to see tools
```

### Web UI Full Implementation
```bash
cd implementations/web-ui-full
./start.sh
# or
docker-compose up -d
```

## Docker Commands

### Docker Compose (any implementation with Docker support)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose build
docker-compose up -d
```

### Docker Production (Stack deployment)
```bash
cd implementations/docker-production

# Build images
./build.sh

# Deploy stack
./install.sh

# Check services
docker stack services sec-llama

# View logs
docker service logs -f sec-llama_web-ui

# Scale services
docker service scale sec-llama_web-ui=3

# Remove stack
docker stack rm sec-llama
```

## Testing Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov=cli --cov=web_ui

# Run specific test file
pytest tests/test_cve_lookup.py

# Verbose output
pytest -v

# Run async tests
pytest -v --asyncio-mode=auto
```

**Note**: No test files found in current repository - tests need to be created.

## Linting & Code Quality
```bash
# Activate virtual environment
source venv/bin/activate

# Python linting
pylint modules/ cli/ web_ui/

# Security scanning
bandit -r modules/ cli/ web_ui/

# Static analysis
semgrep --config auto modules/ cli/

# Dependency vulnerability check
safety check
```

**Note**: No linting configuration files (.pylintrc, .flake8) found yet.

## Development Workflow

### Activate Virtual Environment
```bash
cd implementations/[implementation-name]
source venv/bin/activate
```

### Update Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-full.txt  # For Web UI
```

### Check Ollama Connection
```bash
curl http://localhost:11434/api/tags
```

### View Logs
```bash
# Application logs
tail -f logs/sec-llama.log

# Docker logs
docker-compose logs -f
```

## Git Commands (System: Darwin/macOS)
```bash
# Standard git commands work normally
git status
git add .
git commit -m "message"
git push
git pull

# Current branch
git branch

# View recent commits
git log --oneline -10
```

## System Utilities (Darwin/macOS)
Standard Unix commands available:
- `ls`, `cd`, `pwd` - File navigation
- `grep`, `find` - Search
- `cat`, `less`, `head`, `tail` - File viewing
- `mkdir`, `rm`, `cp`, `mv` - File operations
- `ps`, `top`, `kill` - Process management
- `curl`, `wget` - Network requests

## Configuration Files

### Main Configuration
```bash
# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit configuration
nano config/config.yaml  # or vim, code, etc.
```

### Environment Variables
```bash
# Copy example .env
cp .env.example .env

# Edit environment
nano .env
```

## Common Security Testing Commands (Example)

### Network Scanning
```bash
./sec-llama.sh scan network 192.168.1.0/24
./sec-llama.sh scan ports --host 192.168.1.10 --ai-suggest
./sec-llama.sh scan vuln --network 192.168.1.0/24
```

### Code Analysis
```bash
./sec-llama.sh scan code --path ./myapp --language python
./sec-llama.sh scan container --image nginx:latest
```

### Threat Intelligence
```bash
./sec-llama.sh threat cve CVE-2024-1234
./sec-llama.sh threat ioc 192.168.1.100
./sec-llama.sh threat search --keyword "apache"
```

### Traffic Analysis
```bash
./sec-llama.sh analyze traffic --pcap capture.pcap
```

### LLM Training
```bash
./sec-llama.sh train collect --type cve --max 10000
./sec-llama.sh train finetune --base llama3.1:8b --dataset data.json
```

## Troubleshooting

### Virtual Environment Issues
```bash
rm -rf venv
./setup.sh  # Re-run setup
```

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Port Already in Use
```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Docker Issues
```bash
# Clean up Docker
docker system prune -a

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```
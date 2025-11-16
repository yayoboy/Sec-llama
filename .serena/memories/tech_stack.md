# Sec-Llama - Tech Stack

## Programming Languages
- **Python 3.8+** (main language for all implementations)
- **JavaScript/Vue.js** (for Web UI frontend)
- **Shell/Bash** (setup and start scripts)

## AI/LLM Stack
- **Ollama** (local LLM runtime) - Required
  - Recommended models: llama3.1:8b, llama3.1:70b
  - Default host: http://localhost:11434
- **LangChain** (>=0.1.0) - LLM integration framework
- **LangChain Community** (>=0.0.20) - Community integrations
- **ChromaDB** (>=0.4.0) - Vector database for RAG
- **Sentence Transformers** (>=2.2.0) - Embedding models
  - Default model: all-MiniLM-L6-v2

## Backend Framework
- **FastAPI** (>=0.104.0) - Modern async web framework
- **Uvicorn** (>=0.24.0) - ASGI server
- **Pydantic** (>=2.5.0) - Data validation
- **Python Multipart** (>=0.0.6) - File upload support

## Database & Caching
- **SQLite** - Default for standalone implementations
- **PostgreSQL** (>=2.9.0 via psycopg2-binary) - For production
- **Redis** (>=5.0.0) - Caching layer
- **SQLAlchemy** (>=2.0.0) - ORM

## Security Tools Integration
### Network Security
- **Scapy** (>=2.5.0) - Packet manipulation
- **python-nmap** (>=0.7.1) - Nmap wrapper
- **netaddr** (>=0.9.0) - Network address manipulation
- **PyShark** (>=0.6.0) - Wireshark wrapper for traffic analysis
- **dpkt** (>=1.9.8) - Packet parsing
- **wifi** (>=0.3.8) - Wireless tools
- **dnspython** (>=2.4.0) - DNS toolkit
- **paramiko** (>=3.4.0) - SSH protocol

### Code Security (SAST)
- **bandit** (>=1.7.5) - Python security linting
- **safety** (>=2.3.0) - Dependency vulnerability checking
- **semgrep** (>=1.45.0) - Multi-language static analysis
- **pylint** (>=3.0.0) - Python linting

### Web Security
- **scrapy** (>=2.11.0) - Web scraping
- **selenium** (>=4.15.0) - Browser automation
- **requests** (>=2.31.0) - HTTP library
- **beautifulsoup4** (>=4.12.0) - HTML parsing

### Exploitation & Pentesting
- **pwntools** (>=4.11.0) - CTF/exploitation framework
- **impacket** (>=0.11.0) - Network protocol implementation

## CLI Tools
- **Click** (>=8.1.0) - CLI framework
- **Rich** (>=13.7.0) - Terminal formatting
- **Prompt Toolkit** (>=3.0.0) - Interactive CLI
- **Questionary** (>=2.0.0) - Prompt library
- **Colorama** (>=0.4.6) - Cross-platform colored terminal

## Data Processing
- **Pandas** (>=2.1.0) - Data analysis
- **NumPy** (>=1.24.0) - Numerical computing
- **PyYAML** (>=6.0) - YAML parsing

## Reporting
- **ReportLab** (>=4.0.0) - PDF generation
- **Matplotlib** (>=3.8.0) - Plotting/graphs
- **Jinja2** (>=3.1.0) - Template engine
- **Markdown** (>=3.5.0) - Markdown parsing

## Cryptography
- **cryptography** (>=41.0.0) - Cryptographic primitives
- **pycryptodome** (>=3.19.0) - Cryptographic library

## Utilities
- **python-dotenv** (>=1.0.0) - Environment variables
- **loguru** (>=0.7.0) - Logging
- **tqdm** (>=4.66.0) - Progress bars

## Testing
- **pytest** (>=7.4.0) - Testing framework
- **pytest-cov** (>=4.1.0) - Coverage plugin
- **pytest-asyncio** (>=0.21.0) - Async test support

## Containerization
- **Docker** - Container runtime
- **Docker Compose** - Multi-container orchestration
- **Docker Swarm** - Production deployment (docker-production)

## Frontend (Web UI)
- **Vue.js** - Progressive JavaScript framework
- **Node.js** - JavaScript runtime for build tools

## Default Ports
- **8080** - Web UI
- **8765** - MCP HTTP server
- **11434** - Ollama
- **5432** - PostgreSQL
- **6379** - Redis
- **5050** - pgAdmin (dev environment)
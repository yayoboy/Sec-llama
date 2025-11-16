# 🚀 Quick Start Guide - Sec-Llama LAN Server

Get started in **5 minutes** with Docker Compose or Portainer!

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Docker** installed on your LAN server
- [ ] **Docker Compose** installed
- [ ] **Remote LLM server** configured (Ollama or LM Studio on another PC)
- [ ] Network connectivity between LAN server and LLM server

---

## Step 1: Prepare Remote LLM Server

### Option A: Ollama (Recommended)

**On your LLM server PC** (e.g., 192.168.1.100):

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.1:8b

# Start with network access
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

**Test from LAN server**:
```bash
curl http://192.168.1.100:11434/api/tags
```

### Option B: LM Studio

1. Download and install LM Studio from https://lmstudio.ai/
2. Load a model
3. Go to Settings → Server
4. Set Host: `0.0.0.0`, Port: `1234`
5. Click "Start Server"

**Test from LAN server**:
```bash
curl http://192.168.1.100:1234/v1/models
```

---

## Step 2: Deploy Sec-Llama

### Method 1: Docker Compose (Fastest)

```bash
# 1. Navigate to lan-server directory
cd implementations/lan-server

# 2. Create and edit .env file
cp .env.example .env
nano .env

# REQUIRED: Edit these values in .env:
# - LLM_PROVIDER=ollama
# - OLLAMA_HOST=http://192.168.1.100:11434
# - SECRET_KEY=<generate-random-32-char-string>
# - JWT_SECRET_KEY=<generate-random-32-char-string>
# - POSTGRES_PASSWORD=<secure-password>
# - REDIS_PASSWORD=<secure-password>

# 3. Start all services
docker-compose up -d

# 4. Check status
docker-compose ps
docker-compose logs -f web-ui
```

### Method 2: Portainer Stack

```bash
# 1. Access Portainer
# Open: http://your-portainer-server:9000

# 2. Create new stack
# - Go to: Stacks → Add Stack
# - Name: sec-llama-lan
# - Build method: Web editor

# 3. Copy stack file
# Copy content from: portainer-stack.yml

# 4. Add environment variables
# Click "Add environment variable" for each:

# Required variables (from portainer-env.txt):
LLM_PROVIDER=ollama
OLLAMA_HOST=http://192.168.1.100:11434
OLLAMA_MODEL=llama3.1:8b
SECRET_KEY=your-random-32-char-string
JWT_SECRET_KEY=your-random-32-char-string
POSTGRES_PASSWORD=your-secure-password
REDIS_PASSWORD=your-secure-password
WEB_UI_PORT=8080

# 5. Deploy stack
# Click "Deploy the stack"

# 6. Monitor deployment
# Go to: Containers
# Wait for all containers to be "Running"
```

---

## Step 3: Access Web UI

1. Open browser
2. Navigate to: `http://your-server-ip:8080`
3. You should see the Sec-Llama Web UI

**Default access**:
- URL: `http://localhost:8080` (from server)
- URL: `http://192.168.1.10:8080` (from network)

---

## Step 4: Configure AI in Web UI

1. Go to **AI Configuration** section
2. Select Provider: **Ollama** or **LM Studio**
3. Enter LLM Host: `http://192.168.1.100:11434`
4. Select Model: `llama3.1:8b`
5. Click **Test Connection**
6. If successful, click **Save Configuration**

---

## Step 5: Run Your First Security Scan

### Network Discovery Example

1. Go to **Security Tools** → **Network Security**
2. Click **Host Discovery**
3. Enter network: `192.168.1.0/24`
4. Click **Scan**
5. View results with AI analysis

### CVE Lookup Example

1. Go to **Security Tools** → **Threat Intelligence**
2. Click **CVE Lookup**
3. Enter CVE ID: `CVE-2024-1234`
4. Click **Analyze**
5. View AI-powered analysis

---

## Troubleshooting

### Cannot connect to Web UI

```bash
# Check if container is running
docker-compose ps

# Check logs
docker-compose logs web-ui

# Check port
netstat -tlnp | grep 8080
```

### LLM connection failed

```bash
# From LAN server, test LLM connectivity
ping 192.168.1.100

# Test Ollama API
curl http://192.168.1.100:11434/api/tags

# Test LM Studio API
curl http://192.168.1.100:1234/v1/models

# Check firewall on LLM server
# Ollama: Allow port 11434
# LM Studio: Allow port 1234
```

### Database connection error

```bash
# Check PostgreSQL container
docker-compose logs postgres

# Verify password in .env matches
grep POSTGRES_PASSWORD .env
```

### Permission errors

```bash
# Fix directory permissions
sudo chown -R 1000:1000 logs/ reports/ database/

# Restart containers
docker-compose restart
```

---

## Common Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web-ui
docker-compose logs -f postgres
docker-compose logs -f redis

# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes data)
docker-compose down -v

# Update images
docker-compose pull
docker-compose up -d

# Check resource usage
docker stats
```

---

## Security Checklist

Before production use:

- [ ] Changed all default passwords in `.env`
- [ ] Generated secure random `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configured firewall rules
- [ ] Set up HTTPS (reverse proxy)
- [ ] Configured CORS for specific domains (not `*`)
- [ ] Enabled rate limiting
- [ ] Set up regular database backups
- [ ] Reviewed security modules permissions

---

## Next Steps

1. **Read full documentation**: See `README.md`
2. **Explore security modules**: Try different scanning tools
3. **Configure automated reports**: Set up scheduled scans
4. **Set up backups**: Configure database backup strategy
5. **Enable HTTPS**: Configure reverse proxy (Nginx/Traefik)

---

## Getting Help

- **Documentation**: `README.md` for detailed info
- **Configuration**: Check `.env` and `config.example.yaml`
- **Logs**: `docker-compose logs -f` for debugging
- **Issues**: Report bugs via GitHub Issues

---

**Happy security testing! 🛡️**

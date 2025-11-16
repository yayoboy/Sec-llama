# Deployments

This directory contains all deployment configurations for Sec-Llama.

## 📁 Structure

```
deployments/
├── docker/              # Docker Compose configurations
├── docker-stack/        # Docker Stack (Swarm) configurations
└── live-usb/           # Live USB creation scripts
```

## 🐳 Docker Compose (`docker/`)

Standard Docker Compose files for local development and testing.

**Files:**
- `docker-compose.yml` - Basic setup
- `docker-compose.mcp.yml` - MCP Server deployment
- `docker-compose.web-ui.yml` - Web UI deployment
- `Dockerfile` - Main image
- `Dockerfile.mcp` - MCP Server image
- `Dockerfile.web-ui` - Web UI image

**Usage:**
```bash
cd deployments/docker
docker-compose up -d
```

## 🔄 Docker Stack (`docker-stack/`)

Production-ready Docker Stack for Docker Swarm deployment.

**Features:**
- Multi-service orchestration
- Automatic scaling
- High availability
- Health checks
- Secrets management

**Usage:**
```bash
# Install complete stack
../../scripts/install_stack.sh

# Or manually
cd deployments/docker-stack
docker stack deploy -c docker-stack.yml sec-llama
```

See [DOCKER_STACK_INSTALLATION.md](../../docs/DOCKER_STACK_INSTALLATION.md) for details.

## 💾 Live USB (`live-usb/`)

Scripts to create bootable Live USB with persistence.

**Scripts:**
- `create_persistent_usb.sh` - Create Live USB with persistence partition
- `setup_persistent_env.sh` - Setup environment on Live USB
- `backup_data.sh` - Backup reports and configurations

**Usage:**
```bash
cd deployments/live-usb

# Create Live USB (⚠️ DESTROYS DATA ON DEVICE!)
sudo ./create_persistent_usb.sh /dev/sdX

# Setup environment after boot
./setup_persistent_env.sh
```

See [LIVE_USB.md](../../docs/LIVE_USB.md) for details.

---

## 🚀 Quick Start

### Development (Docker Compose)
```bash
cd deployments/docker
docker-compose -f docker-compose.web-ui.yml up -d
```

### Production (Docker Stack)
```bash
../../scripts/install_stack.sh --with-nginx --with-backup
```

### Live USB
```bash
cd deployments/live-usb
sudo ./create_persistent_usb.sh /dev/sdX
```

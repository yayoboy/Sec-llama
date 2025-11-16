#!/bin/bash

# Sec-Llama Docker Stack Installation Script
# Automated deployment with all dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
STACK_NAME="sec-llama"
ENV_FILE="$PROJECT_ROOT/.env"
WITH_NGINX=false
WITH_BACKUP=false
SWARM_INIT=true

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         Sec-Llama Stack Installer                        ║
║         Complete Docker Stack Deployment                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Help function
show_help() {
    cat << 'HELP'
Usage: install_stack.sh [OPTIONS]

Install Sec-Llama Docker Stack with all dependencies

OPTIONS:
    --stack-name NAME       Stack name (default: sec-llama)
    --with-nginx            Include Nginx reverse proxy
    --with-backup           Include automatic backup service
    --no-swarm-init         Skip Docker Swarm initialization
    -h, --help              Show this help message

EXAMPLES:
    # Basic installation
    ./scripts/install_stack.sh

    # With Nginx and backup
    ./scripts/install_stack.sh --with-nginx --with-backup

    # Custom stack name
    ./scripts/install_stack.sh --stack-name my-security-suite

HELP
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --stack-name)
            STACK_NAME="$2"
            shift 2
            ;;
        --with-nginx)
            WITH_NGINX=true
            shift
            ;;
        --with-backup)
            WITH_BACKUP=true
            shift
            ;;
        --no-swarm-init)
            SWARM_INIT=false
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Function to print step
print_step() {
    echo ""
    echo -e "${BLUE}>>> $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker not found. Please install Docker first."
    exit 1
fi
print_success "Docker found: $(docker --version)"

# Check Docker version
DOCKER_VERSION=$(docker version --format '{{.Server.Version}}')
print_success "Docker version: $DOCKER_VERSION"

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]] && ! groups | grep -q docker; then
    print_warning "User not in docker group. You may need to run with sudo."
fi

# Initialize Docker Swarm
print_step "Configuring Docker Swarm..."

if docker info 2>/dev/null | grep -q "Swarm: active"; then
    print_success "Docker Swarm already active"
else
    if [ "$SWARM_INIT" = true ]; then
        print_warning "Initializing Docker Swarm..."
        docker swarm init || {
            print_error "Failed to initialize Docker Swarm"
            exit 1
        }
        print_success "Docker Swarm initialized"
    else
        print_error "Docker Swarm not active and --no-swarm-init specified"
        exit 1
    fi
fi

# Create .env file
print_step "Creating environment configuration..."

if [ -f "$ENV_FILE" ]; then
    print_warning ".env file already exists. Backing up..."
    cp "$ENV_FILE" "$ENV_FILE.backup.$(date +%s)"
fi

# Generate secure passwords
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

POSTGRES_PASSWORD=$(generate_password)
REDIS_PASSWORD=$(generate_password)
SECRET_KEY=$(generate_password)

cat > "$ENV_FILE" << EOF
# Sec-Llama Stack Configuration
# Generated on $(date)

# Stack Configuration
STACK_NAME=$STACK_NAME

# Database Configuration
POSTGRES_PASSWORD=$POSTGRES_PASSWORD

# Redis Configuration
REDIS_PASSWORD=$REDIS_PASSWORD

# Web UI Secret Key
SECRET_KEY=$SECRET_KEY

# Ollama Configuration
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.1:8b
DEFAULT_MODEL=llama3.1:8b

# MCP Server Configuration
MCP_PORT=8765
MCP_API_KEYS=

# Web UI Configuration
WEB_UI_PORT=8080

# Nginx Configuration (if using)
HTTP_PORT=80
HTTPS_PORT=443

# Security
ALLOWED_NETWORKS=0.0.0.0/0
ALLOWED_ORIGINS=*
REQUIRE_CONFIRMATION=false

# Backup Configuration
BACKUP_SCHEDULE=0 2 * * *

# Logging
LOG_LEVEL=INFO
EOF

print_success "Environment file created: $ENV_FILE"

# Source the environment file
source "$ENV_FILE"

# Create Docker secrets
print_step "Creating Docker secrets..."

# Function to create or update secret
create_secret() {
    local secret_name=$1
    local secret_value=$2

    if docker secret ls | grep -q "$secret_name"; then
        print_warning "Secret $secret_name already exists, removing..."
        docker secret rm "$secret_name" 2>/dev/null || true
    fi

    echo "$secret_value" | docker secret create "$secret_name" - || {
        print_error "Failed to create secret: $secret_name"
        return 1
    }
    print_success "Created secret: $secret_name"
}

create_secret "postgres_password" "$POSTGRES_PASSWORD"
create_secret "redis_password" "$REDIS_PASSWORD"
create_secret "secret_key" "$SECRET_KEY"

# Create necessary directories
print_step "Creating directories..."

mkdir -p "$PROJECT_ROOT"/{config,logs,reports,database,backups,nginx/ssl}
print_success "Directories created"

# Create backup script
print_step "Creating backup script..."

cat > "$PROJECT_ROOT/scripts/backup.sh" << 'BACKUP_SCRIPT'
#!/bin/sh
# Database backup script

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
BACKUP_FILE="$BACKUP_DIR/sec_llama_backup_$TIMESTAMP.sql.gz"

echo "Starting backup at $(date)"

# Perform backup
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump \
    -h "$POSTGRES_HOST" \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB" \
    | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup completed: $BACKUP_FILE"

    # Keep only last 7 backups
    ls -t $BACKUP_DIR/sec_llama_backup_*.sql.gz | tail -n +8 | xargs rm -f 2>/dev/null || true
    echo "Old backups cleaned up"
else
    echo "Backup failed!"
    exit 1
fi
BACKUP_SCRIPT

chmod +x "$PROJECT_ROOT/scripts/backup.sh"
print_success "Backup script created"

# Create Nginx configuration
if [ "$WITH_NGINX" = true ]; then
    print_step "Creating Nginx configuration..."

    mkdir -p "$PROJECT_ROOT/nginx"

    cat > "$PROJECT_ROOT/nginx/nginx.conf" << 'NGINX_CONF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=50r/s;

    # Upstream servers
    upstream web_ui {
        server web-ui:8080;
    }

    upstream mcp_server {
        server mcp-server:8765;
    }

    # HTTP server (redirect to HTTPS)
    server {
        listen 80;
        server_name _;

        location / {
            return 301 https://$host$request_uri;
        }
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name _;

        # SSL configuration (use your own certificates)
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Web UI
        location / {
            proxy_pass http://web_ui;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            limit_req zone=general_limit burst=20 nodelay;
        }

        # WebSocket support
        location /ws {
            proxy_pass http://web_ui;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # MCP Server API
        location /mcp/ {
            proxy_pass http://mcp_server/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            limit_req zone=api_limit burst=5 nodelay;
        }

        # Health checks
        location /health {
            access_log off;
            return 200 "OK";
            add_header Content-Type text/plain;
        }
    }
}
NGINX_CONF

    print_success "Nginx configuration created"
    print_warning "Note: You need to provide SSL certificates in nginx/ssl/"
fi

# Build Docker images
print_step "Building Docker images..."

cd "$PROJECT_ROOT"

docker build -t sec-llama/mcp-server:latest -f Dockerfile.mcp . || {
    print_error "Failed to build MCP server image"
    exit 1
}
print_success "MCP server image built"

docker build -t sec-llama/web-ui:latest -f Dockerfile.web-ui . || {
    print_error "Failed to build Web UI image"
    exit 1
}
print_success "Web UI image built"

# Deploy stack
print_step "Deploying Docker Stack..."

DEPLOY_CMD="docker stack deploy -c docker-stack.yml"

if [ "$WITH_NGINX" = true ]; then
    DEPLOY_CMD="$DEPLOY_CMD --with-registry-auth"
fi

# Add profiles
PROFILES=""
[ "$WITH_NGINX" = true ] && PROFILES="$PROFILES,with-nginx"
[ "$WITH_BACKUP" = true ] && PROFILES="$PROFILES,with-backup"

if [ -n "$PROFILES" ]; then
    export COMPOSE_PROFILES="${PROFILES#,}"
fi

$DEPLOY_CMD "$STACK_NAME" || {
    print_error "Failed to deploy stack"
    exit 1
}

print_success "Stack deployed: $STACK_NAME"

# Wait for services
print_step "Waiting for services to start..."

sleep 10

# Check service status
print_step "Checking service status..."

docker stack services "$STACK_NAME"

# Show access information
print_step "Installation Complete!"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║         Sec-Llama Stack Installed Successfully!          ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Access Points:${NC}"
echo -e "  Web UI:     ${GREEN}http://localhost:$WEB_UI_PORT${NC}"
echo -e "  MCP Server: ${GREEN}http://localhost:$MCP_PORT${NC}"
echo -e "  Ollama:     ${GREEN}http://localhost:$OLLAMA_PORT${NC}"
if [ "$WITH_NGINX" = true ]; then
    echo -e "  Nginx:      ${GREEN}https://localhost:$HTTPS_PORT${NC}"
fi
echo ""
echo -e "${BLUE}Credentials:${NC}"
echo -e "  Saved in: ${YELLOW}$ENV_FILE${NC}"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo -e "  View services:  ${YELLOW}docker stack services $STACK_NAME${NC}"
echo -e "  View logs:      ${YELLOW}docker service logs -f ${STACK_NAME}_web-ui${NC}"
echo -e "  Remove stack:   ${YELLOW}docker stack rm $STACK_NAME${NC}"
echo -e "  Scale service:  ${YELLOW}docker service scale ${STACK_NAME}_web-ui=3${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Configure AI settings in Web UI: ${GREEN}http://localhost:$WEB_UI_PORT/config${NC}"
echo -e "  2. Create API keys in Web UI: ${GREEN}http://localhost:$WEB_UI_PORT/api-keys${NC}"
echo -e "  3. Start using security tools!"
echo ""
echo -e "${YELLOW}Note: It may take a few minutes for Ollama to pull the default model.${NC}"
echo ""

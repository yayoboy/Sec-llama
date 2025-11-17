#!/bin/bash
# ================================================================================
# Sec-Llama - Environment Variables Validation Script
# ================================================================================
#
# This script validates your .env file before deployment
# Usage: ./validate-env.sh
#
# ================================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

echo "================================================================================"
echo "Sec-Llama - Environment Validation"
echo "================================================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    echo "Please run: cp .env.example .env"
    exit 1
fi

echo -e "${GREEN}✓ .env file found${NC}"
echo ""

# Source .env
set -a
source .env
set +a

# Function to check if variable is set and not default
check_required() {
    local var_name=$1
    local default_value=$2
    local current_value="${!var_name}"

    if [ -z "$current_value" ]; then
        echo -e "${RED}✗ ERROR: $var_name is not set${NC}"
        ((ERRORS++))
        return 1
    fi

    if [ "$current_value" == "$default_value" ] || [[ "$current_value" == *"CHANGE_ME"* ]] || [[ "$current_value" == *"CAMBIAMI"* ]]; then
        echo -e "${RED}✗ ERROR: $var_name still has default value: $current_value${NC}"
        echo "  Generate secure value with: openssl rand -hex 32"
        ((ERRORS++))
        return 1
    fi

    echo -e "${GREEN}✓ $var_name is set${NC}"
    return 0
}

# Function to check optional variable
check_optional() {
    local var_name=$1
    local current_value="${!var_name}"

    if [ -z "$current_value" ]; then
        echo -e "${YELLOW}⚠ WARNING: $var_name is not set (optional)${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓ $var_name is set${NC}"
    fi
}

# Function to validate IP address
validate_ip() {
    local var_name=$1
    local value="${!var_name}"

    if [[ $value =~ ^https?://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]+$ ]]; then
        echo -e "${GREEN}✓ $var_name format is valid${NC}"
    else
        echo -e "${YELLOW}⚠ WARNING: $var_name format might be invalid: $value${NC}"
        echo "  Expected format: http://192.168.1.100:11434"
        ((WARNINGS++))
    fi
}

# Function to check key length
check_key_length() {
    local var_name=$1
    local min_length=$2
    local current_value="${!var_name}"

    if [ ${#current_value} -lt $min_length ]; then
        echo -e "${RED}✗ ERROR: $var_name is too short (${#current_value} chars, minimum $min_length)${NC}"
        echo "  Generate with: openssl rand -hex 32"
        ((ERRORS++))
        return 1
    fi

    echo -e "${GREEN}✓ $var_name length is sufficient (${#current_value} chars)${NC}"
    return 0
}

echo "Checking Required Variables..."
echo "--------------------------------------------------------------------------------"

# Database
check_required "POSTGRES_PASSWORD" ""
check_required "POSTGRES_DB" ""
check_required "POSTGRES_USER" ""

# Redis
check_required "REDIS_PASSWORD" ""

# LLM
check_required "OLLAMA_HOST" ""
validate_ip "OLLAMA_HOST"

# Security Keys
echo ""
echo "Checking Security Keys..."
echo "--------------------------------------------------------------------------------"
check_required "SECRET_KEY" ""
check_key_length "SECRET_KEY" 32

check_required "JWT_SECRET_KEY" ""
check_key_length "JWT_SECRET_KEY" 32

check_required "ADMIN_PASSWORD" "ChangeMeOnFirstLogin123!"

echo ""
echo "Checking Optional Variables..."
echo "--------------------------------------------------------------------------------"

check_optional "OLLAMA_MODEL"
check_optional "DEBUG"
check_optional "LOG_LEVEL"
check_optional "WEB_UI_PORT"

# Test OLLAMA connection
echo ""
echo "Testing LLM Connection..."
echo "--------------------------------------------------------------------------------"

if command -v curl &> /dev/null; then
    if curl -s -f "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Successfully connected to Ollama at $OLLAMA_HOST${NC}"
        echo "  Available models:"
        curl -s "$OLLAMA_HOST/api/tags" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | sed 's/^/    - /'
    else
        echo -e "${YELLOW}⚠ WARNING: Cannot connect to Ollama at $OLLAMA_HOST${NC}"
        echo "  Please ensure:"
        echo "  1. Ollama is running on the remote PC"
        echo "  2. OLLAMA_HOST is set to 0.0.0.0:11434 on the Ollama server"
        echo "  3. Firewall allows port 11434"
        echo "  4. IP address in .env is correct"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠ WARNING: curl not found, skipping Ollama connection test${NC}"
    ((WARNINGS++))
fi

# Check Docker
echo ""
echo "Checking Docker..."
echo "--------------------------------------------------------------------------------"

if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker is installed${NC}"
    docker --version
else
    echo -e "${RED}✗ ERROR: Docker is not installed${NC}"
    ((ERRORS++))
fi

if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
    echo -e "${GREEN}✓ Docker Compose is available${NC}"
    docker compose version 2>/dev/null || docker-compose --version
else
    echo -e "${RED}✗ ERROR: Docker Compose is not installed${NC}"
    ((ERRORS++))
fi

# Check disk space
echo ""
echo "Checking System Resources..."
echo "--------------------------------------------------------------------------------"

if command -v df &> /dev/null; then
    AVAILABLE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$AVAILABLE_SPACE" -lt 10 ]; then
        echo -e "${YELLOW}⚠ WARNING: Low disk space (${AVAILABLE_SPACE}GB available)${NC}"
        echo "  Recommended: At least 20GB free space"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓ Sufficient disk space (${AVAILABLE_SPACE}GB available)${NC}"
    fi
fi

# Summary
echo ""
echo "================================================================================"
echo "Validation Summary"
echo "================================================================================"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Your environment is ready for deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. docker-compose up -d"
    echo "  2. docker-compose logs -f web-ui"
    echo "  3. Open http://localhost:8080"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation completed with ${WARNINGS} warning(s)${NC}"
    echo "  You can proceed with deployment, but review the warnings above."
    exit 0
else
    echo -e "${RED}✗ Validation failed with ${ERRORS} error(s) and ${WARNINGS} warning(s)${NC}"
    echo ""
    echo "Please fix the errors above before deploying."
    echo ""
    echo "Quick fixes:"
    echo "  - Generate SECRET_KEY: export SECRET_KEY=\$(openssl rand -hex 32)"
    echo "  - Generate JWT_SECRET_KEY: export JWT_SECRET_KEY=\$(openssl rand -hex 32)"
    echo "  - Update .env file with generated values"
    exit 1
fi

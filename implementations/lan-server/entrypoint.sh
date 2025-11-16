#!/bin/bash
set -e

# ============================================================================
# Sec-Llama Docker Entrypoint Script
#
# Handles:
# - Database connection waiting
# - Alembic migrations
# - Default admin user creation
# - Directory setup
# - Application startup
# ============================================================================

echo "============================================"
echo "Sec-Llama LAN Server - Starting..."
echo "============================================"

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

# Database
DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${POSTGRES_USER:-sec_llama}"
DB_PASSWORD="${POSTGRES_PASSWORD:-sec_llama}"
DB_NAME="${POSTGRES_DB:-sec_llama}"

# Admin user (created on first run)
ADMIN_USERNAME="${ADMIN_USERNAME:-admin}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@sec-llama.local}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-ChangeMeOnFirstLogin123!}"

# Application
APP_HOST="${APP_HOST:-0.0.0.0}"
APP_PORT="${WEB_UI_PORT:-8080}"
WORKERS="${WORKERS:-1}"

# ============================================================================
# FUNCTIONS
# ============================================================================

# Wait for PostgreSQL to be ready
wait_for_postgres() {
    echo "⏳ Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" > /dev/null 2>&1; then
            echo "✅ PostgreSQL is ready!"
            return 0
        fi

        echo "   Attempt $attempt/$max_attempts - PostgreSQL not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "❌ ERROR: PostgreSQL failed to become ready after $max_attempts attempts"
    exit 1
}

# Wait for Redis to be ready
wait_for_redis() {
    echo "⏳ Waiting for Redis at ${REDIS_HOST:-redis}:${REDIS_PORT:-6379}..."

    local redis_host="${REDIS_HOST:-redis}"
    local redis_port="${REDIS_PORT:-6379}"
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if timeout 2 bash -c "echo > /dev/tcp/$redis_host/$redis_port" 2>/dev/null; then
            echo "✅ Redis is ready!"
            return 0
        fi

        echo "   Attempt $attempt/$max_attempts - Redis not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "⚠️  WARNING: Redis failed to become ready after $max_attempts attempts"
    echo "   Continuing anyway (Redis is optional for basic functionality)"
}

# Run database migrations
run_migrations() {
    echo "🔄 Running database migrations..."

    if alembic upgrade head; then
        echo "✅ Database migrations completed successfully"
    else
        echo "❌ ERROR: Database migrations failed"
        exit 1
    fi
}

# Create default admin user if not exists
create_default_admin() {
    echo "👤 Checking for default admin user..."

    python3 - <<EOF
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Setup database connection
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'sec_llama')}:{os.getenv('POSTGRES_PASSWORD', 'sec_llama')}@{os.getenv('DB_HOST', 'postgres')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'sec_llama')}"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # Check if admin user exists
    result = db.execute("SELECT COUNT(*) FROM users WHERE username = '${ADMIN_USERNAME}'")
    count = result.scalar()

    if count == 0:
        # Create password hash
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash("${ADMIN_PASSWORD}")

        # Insert admin user
        db.execute("""
            INSERT INTO users (username, email, hashed_password, full_name, role, is_active, is_superuser)
            VALUES (:username, :email, :password, :full_name, 'admin', true, true)
        """, {
            'username': '${ADMIN_USERNAME}',
            'email': '${ADMIN_EMAIL}',
            'password': hashed_password,
            'full_name': 'System Administrator'
        })
        db.commit()

        print("✅ Default admin user created successfully")
        print(f"   Username: ${ADMIN_USERNAME}")
        print(f"   Email: ${ADMIN_EMAIL}")
        print(f"   Password: ${ADMIN_PASSWORD}")
        print("   ⚠️  IMPORTANT: Change the default password on first login!")
    else:
        print("ℹ️  Admin user already exists, skipping creation")

    db.close()
    sys.exit(0)

except Exception as e:
    print(f"❌ ERROR creating admin user: {e}")
    sys.exit(1)
EOF

    if [ $? -ne 0 ]; then
        echo "⚠️  WARNING: Failed to create default admin user"
        echo "   You may need to create it manually"
    fi
}

# Create necessary directories
create_directories() {
    echo "📁 Creating necessary directories..."

    local dirs=(
        "/app/logs"
        "/app/reports"
        "/app/database"
        "/app/uploads"
        "/app/backups"
    )

    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "   Created: $dir"
        fi
    done

    # Set proper permissions
    chmod -R 755 /app/logs /app/reports /app/uploads /app/backups 2>/dev/null || true

    echo "✅ Directories ready"
}

# Check LLM connectivity (optional, non-blocking)
check_llm_connectivity() {
    echo "🤖 Checking LLM connectivity..."

    local llm_provider="${LLM_PROVIDER:-ollama}"
    local llm_host=""

    if [ "$llm_provider" = "ollama" ]; then
        llm_host="${OLLAMA_HOST:-http://localhost:11434}"
    elif [ "$llm_provider" = "lm-studio" ]; then
        llm_host="${LM_STUDIO_HOST:-http://localhost:1234}"
    else
        echo "ℹ️  LLM provider: $llm_provider (skipping connectivity check)"
        return 0
    fi

    # Extract host and port from URL
    local host_port=$(echo "$llm_host" | sed -e 's|^[^/]*//||' -e 's|/.*$||')

    if timeout 3 curl -sf "$llm_host/api/tags" > /dev/null 2>&1 || \
       timeout 3 curl -sf "$llm_host/v1/models" > /dev/null 2>&1; then
        echo "✅ LLM server is reachable at $llm_host"
    else
        echo "⚠️  WARNING: LLM server at $llm_host is not reachable"
        echo "   This is OK - you can configure it later via Web UI"
    fi
}

# Display startup info
display_startup_info() {
    echo ""
    echo "============================================"
    echo "🚀 Sec-Llama is starting..."
    echo "============================================"
    echo "Environment:"
    echo "  - Database: postgresql://${DB_USER}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
    echo "  - Redis: ${REDIS_HOST:-redis}:${REDIS_PORT:-6379}"
    echo "  - LLM Provider: ${LLM_PROVIDER:-ollama}"
    echo "  - Web UI: http://${APP_HOST}:${APP_PORT}"
    echo "  - Workers: ${WORKERS}"
    echo ""
    echo "Access points:"
    echo "  - Web UI: http://localhost:${APP_PORT}"
    echo "  - API Docs: http://localhost:${APP_PORT}/docs"
    echo "  - Health Check: http://localhost:${APP_PORT}/health"
    echo "============================================"
    echo ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    echo ""

    # Wait for dependencies
    wait_for_postgres
    wait_for_redis

    # Create directories
    create_directories

    # Run database migrations
    run_migrations

    # Create default admin user
    create_default_admin

    # Check LLM (non-blocking)
    check_llm_connectivity

    # Display startup info
    display_startup_info

    # Start application
    echo "🎯 Starting FastAPI application..."
    echo ""

    # Use uvicorn with proper settings
    exec uvicorn web_ui.backend.main:app \
        --host "${APP_HOST}" \
        --port "${APP_PORT}" \
        --workers "${WORKERS}" \
        --log-level "${LOG_LEVEL:-info}" \
        --access-log \
        --use-colors
}

# ============================================================================
# RUN
# ============================================================================

main "$@"

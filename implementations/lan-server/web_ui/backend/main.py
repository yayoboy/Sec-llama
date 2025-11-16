"""
Sec-Llama Web UI - FastAPI Backend

Main application entry point for the Web UI backend.
Provides REST API and WebSocket support for the frontend.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from web_ui.backend.routers import (
    dashboard,
    tools,
    config,
    api_keys,
    audit_logs,
    websocket,
    ai_config
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application state
app_state: Dict[str, Any] = {
    "start_time": datetime.utcnow(),
    "version": "1.0.0"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("Starting Sec-Llama Web UI Backend")
    logger.info(f"Version: {app_state['version']}")

    # Startup tasks
    app.state.start_time = app_state["start_time"]
    app.state.version = app_state["version"]

    yield

    # Shutdown tasks
    logger.info("Shutting down Sec-Llama Web UI Backend")


# Create FastAPI application
app = FastAPI(
    title="Sec-Llama Web UI API",
    description="Backend API for Sec-Llama MCP Server Web Interface",
    version=app_state["version"],
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(tools.router, prefix="/api/tools", tags=["Tools"])
app.include_router(config.router, prefix="/api/config", tags=["Configuration"])
app.include_router(api_keys.router, prefix="/api/api-keys", tags=["API Keys"])
app.include_router(audit_logs.router, prefix="/api/audit-logs", tags=["Audit Logs"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
app.include_router(ai_config.router, prefix="/api/ai", tags=["AI Configuration"])


@app.get("/")
async def root():
    """Root endpoint - serves frontend or API info"""
    return {
        "name": "Sec-Llama Web UI API",
        "version": app_state["version"],
        "status": "running",
        "uptime_seconds": (datetime.utcnow() - app_state["start_time"]).total_seconds()
    }


@app.get("/health")
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.utcnow() - app_state["start_time"]).total_seconds()

    # Test connections
    health_status = {
        "status": "healthy",
        "version": app_state["version"],
        "uptime_seconds": uptime,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "healthy",
            "database": "unknown",  # Will be updated by middleware
            "redis": "unknown",
            "llm": "unknown"
        }
    }

    # Try to check LLM connection
    try:
        from core.llm_interface import get_llm
        llm = get_llm()
        test_result = llm.test_connection()
        health_status["services"]["llm"] = test_result.get("status", "unknown")
    except Exception:
        health_status["services"]["llm"] = "error"

    return health_status


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "title": "Sec-Llama Web UI API",
        "version": app_state["version"],
        "endpoints": {
            "dashboard": "/api/dashboard",
            "tools": "/api/tools",
            "config": "/api/config",
            "api_keys": "/api/api-keys",
            "audit_logs": "/api/audit-logs",
            "websocket": "/ws"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Serve frontend static files (after building Vue app)
# app.mount("/", StaticFiles(directory="web_ui/frontend/dist", html=True), name="frontend")


def main(
    host: str = "0.0.0.0",
    port: int = 8080,
    reload: bool = False
):
    """Run the FastAPI application"""
    uvicorn.run(
        "web_ui.backend.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sec-Llama Web UI Backend")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    main(host=args.host, port=args.port, reload=args.reload)

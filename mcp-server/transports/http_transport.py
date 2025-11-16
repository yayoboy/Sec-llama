"""
HTTP/SSE Transport for MCP Server

Enables remote communication via HTTP Server-Sent Events (for LAN access)
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse
import uvicorn

from mcp.server import Server
from mcp.server.sse import SseServerTransport
import mcp.types as types

logger = logging.getLogger("sec-llama-mcp.http")


class HTTPTransport:
    """
    HTTP/SSE Transport for MCP Server

    Provides remote access to MCP server via HTTP with Server-Sent Events.
    Suitable for LAN deployments where multiple clients need access.
    """

    def __init__(
        self,
        server: Server,
        host: str = "0.0.0.0",
        port: int = 8765,
        api_keys: Optional[list[str]] = None,
        cors_origins: Optional[list[str]] = None
    ):
        """
        Initialize HTTP transport

        Args:
            server: MCP Server instance
            host: Host to bind (default: 0.0.0.0 for all interfaces)
            port: Port to listen on (default: 8765)
            api_keys: List of valid API keys for authentication
            cors_origins: List of allowed CORS origins
        """
        self.server = server
        self.host = host
        self.port = port
        self.api_keys = api_keys or []
        self.cors_origins = cors_origins or ["*"]

        # Create FastAPI app
        self.app = FastAPI(
            title="Sec-Llama MCP Server",
            description="Security Testing via Model Context Protocol",
            version="1.0.0"
        )

        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routes
        self._register_routes()

        logger.info(f"HTTP transport initialized on {host}:{port}")

    def _verify_api_key(self, x_api_key: Optional[str] = Header(None)) -> str:
        """
        Verify API key authentication

        Args:
            x_api_key: API key from X-API-Key header

        Returns:
            Verified API key

        Raises:
            HTTPException: If API key is invalid
        """
        if not self.api_keys:
            # No authentication required
            return "anonymous"

        if not x_api_key:
            raise HTTPException(
                status_code=401,
                detail="Missing X-API-Key header"
            )

        if x_api_key not in self.api_keys:
            logger.warning(f"Invalid API key attempt: {x_api_key[:8]}...")
            raise HTTPException(
                status_code=403,
                detail="Invalid API key"
            )

        logger.info(f"Authenticated with API key: {x_api_key[:8]}...")
        return x_api_key

    def _register_routes(self):
        """Register HTTP routes"""

        @self.app.get("/")
        async def root():
            """Server info endpoint"""
            return {
                "name": "Sec-Llama MCP Server",
                "version": "1.0.0",
                "transport": "HTTP/SSE",
                "status": "running",
                "endpoints": {
                    "sse": "/sse",
                    "health": "/health",
                    "tools": "/tools"
                }
            }

        @self.app.get("/health")
        async def health():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "server": "running"
            }

        @self.app.get("/tools")
        async def list_tools(api_key: str = Depends(self._verify_api_key)):
            """List available MCP tools"""
            try:
                tools = await self.server.list_tools()
                return {
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": tool.inputSchema
                        }
                        for tool in tools
                    ]
                }
            except Exception as e:
                logger.error(f"Error listing tools: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/sse")
        async def sse_endpoint(
            request: Request,
            api_key: str = Depends(self._verify_api_key)
        ):
            """
            SSE endpoint for MCP communication

            This is the main endpoint for MCP clients to connect to.
            Uses Server-Sent Events for bi-directional communication.
            """
            logger.info(f"New SSE connection from {request.client.host}")

            try:
                # Create SSE transport
                transport = SseServerTransport("/messages")

                async def event_generator():
                    """Generate SSE events"""
                    try:
                        async with transport.connect_sse(
                            request.scope,
                            request.receive,
                            request._send
                        ) as (read_stream, write_stream):

                            # Run MCP server with streams
                            init_options = self.server.create_initialization_options()
                            await self.server.run(
                                read_stream,
                                write_stream,
                                init_options
                            )

                    except Exception as e:
                        logger.error(f"SSE stream error: {e}", exc_info=True)
                        yield {
                            "event": "error",
                            "data": str(e)
                        }

                return EventSourceResponse(event_generator())

            except Exception as e:
                logger.error(f"SSE endpoint error: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            """Global exception handler"""
            logger.error(f"Unhandled exception: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"error": str(exc)}
            )

    async def run(self):
        """Run HTTP server"""
        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=True
        )

        server = uvicorn.Server(config)

        logger.info(f"Starting HTTP/SSE server on http://{self.host}:{self.port}")
        logger.info(f"SSE endpoint: http://{self.host}:{self.port}/sse")
        logger.info(f"Tools list: http://{self.host}:{self.port}/tools")

        if self.api_keys:
            logger.info(f"Authentication: ENABLED ({len(self.api_keys)} API keys)")
        else:
            logger.warning("Authentication: DISABLED (not recommended for production)")

        await server.serve()


async def run_http_transport(
    server: Server,
    host: str = "0.0.0.0",
    port: int = 8765,
    api_keys: Optional[list[str]] = None,
    cors_origins: Optional[list[str]] = None
):
    """
    Run MCP server with HTTP/SSE transport

    Args:
        server: Initialized MCP Server instance
        host: Host to bind
        port: Port to listen on
        api_keys: List of valid API keys
        cors_origins: List of allowed CORS origins
    """
    transport = HTTPTransport(
        server=server,
        host=host,
        port=port,
        api_keys=api_keys,
        cors_origins=cors_origins
    )

    await transport.run()


async def main():
    """
    Standalone HTTP transport for testing

    Usage:
        python -m mcp_server.transports.http_transport

    Environment variables:
        MCP_API_KEYS: Comma-separated list of API keys
        MCP_HOST: Host to bind (default: 0.0.0.0)
        MCP_PORT: Port to listen (default: 8765)
    """
    import os
    from mcp_server.server import SecLlamaMCPServer

    # Get configuration from environment
    api_keys_str = os.getenv("MCP_API_KEYS", "")
    api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8765"))

    logger.info(f"Configuration:")
    logger.info(f"  Host: {host}")
    logger.info(f"  Port: {port}")
    logger.info(f"  API Keys: {len(api_keys) if api_keys else 'None (auth disabled)'}")

    # Initialize server
    mcp_server = SecLlamaMCPServer()

    # Run HTTP transport
    await run_http_transport(
        server=mcp_server.server,
        host=host,
        port=port,
        api_keys=api_keys
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("HTTP transport stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

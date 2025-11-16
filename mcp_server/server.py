#!/usr/bin/env python3
"""
Sec-Llama MCP Server
Exposes security testing capabilities via Model Context Protocol
"""

import asyncio
import sys
import logging
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types

from core.config import get_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sec-llama-mcp")


class SecLlamaMCPServer:
    """
    Sec-Llama MCP Server

    Exposes security testing tools via MCP protocol for use with
    Claude and other MCP-compatible clients.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize MCP server"""
        self.server = Server("sec-llama")
        self.config = get_config()

        logger.info("Initializing Sec-Llama MCP Server...")
        logger.info(f"LLM Provider: {self.config.llm.provider}")
        logger.info(f"LLM Model: {self.config.llm.model}")

        # Register all tools
        self._register_tools()

        logger.info("Sec-Llama MCP Server initialized successfully")

    def _register_tools(self):
        """Register all MCP tools"""
        from mcp_server.tools import (
            network_tools,
            code_tools,
            threat_tools,
        )

        # Register tools from each module
        logger.info("Registering MCP tools...")

        network_tools.register(self.server)
        logger.info("✓ Network tools registered")

        code_tools.register(self.server)
        logger.info("✓ Code security tools registered")

        threat_tools.register(self.server)
        logger.info("✓ Threat intelligence tools registered")

        # TODO: Register additional tool modules as they are implemented
        # pentest_tools.register(self.server)
        # agent_tools.register(self.server)
        # logs_tools.register(self.server)
        # incident_tools.register(self.server)
        # training_tools.register(self.server)

        logger.info(f"Total tools registered: {len(self.server.list_tools())}")

    async def run_stdio(self):
        """Run server with stdio transport (for local use)"""
        from mcp_server.transports.stdio_transport import run_stdio_transport
        await run_stdio_transport(self.server)

    async def run_http(self, host: str = "0.0.0.0", port: int = 8765, api_keys: Optional[list[str]] = None):
        """Run server with HTTP/SSE transport (for LAN use)"""
        from mcp_server.transports.http_transport import run_http_transport
        await run_http_transport(
            server=self.server,
            host=host,
            port=port,
            api_keys=api_keys
        )


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sec-Llama MCP Server - Security Testing via Model Context Protocol"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport method (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port for HTTP server (default: 8765)"
    )
    parser.add_argument(
        "--config",
        help="Path to MCP server config file"
    )
    parser.add_argument(
        "--api-keys",
        help="Comma-separated list of API keys for HTTP authentication"
    )

    args = parser.parse_args()

    # Initialize server
    server = SecLlamaMCPServer(config_path=args.config)

    # Parse API keys
    api_keys = None
    if args.api_keys:
        api_keys = [k.strip() for k in args.api_keys.split(",") if k.strip()]
        logger.info(f"Loaded {len(api_keys)} API keys")

    # Run with selected transport
    if args.transport == "stdio":
        await server.run_stdio()
    elif args.transport == "http":
        await server.run_http(host=args.host, port=args.port, api_keys=api_keys)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

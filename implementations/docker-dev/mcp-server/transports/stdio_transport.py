"""
Stdio Transport for MCP Server

Enables local communication via stdin/stdout (for Claude Desktop, CLI)
"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.server.stdio import stdio_server
from mcp.server import Server
import mcp.types as types

logger = logging.getLogger("sec-llama-mcp.stdio")


async def run_stdio_transport(server: Server):
    """
    Run MCP server with stdio transport

    This transport is used for local communication, typically with:
    - Claude Desktop application
    - Claude CLI
    - Other MCP clients on the same machine

    Communication happens via stdin/stdout, making it suitable for
    subprocess-based integrations.

    Args:
        server: Initialized MCP Server instance
    """
    logger.info("Starting MCP server with stdio transport...")
    logger.info("Waiting for client connection on stdin/stdout...")

    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Client connected via stdio")

            # Create initialization options
            init_options = server.create_initialization_options()

            # Run server with streams
            await server.run(
                read_stream,
                write_stream,
                init_options
            )

    except Exception as e:
        logger.error(f"Stdio transport error: {e}", exc_info=True)
        raise


async def main():
    """
    Standalone stdio transport for testing

    Usage:
        python -m mcp_server.transports.stdio_transport
    """
    from mcp_server.server import SecLlamaMCPServer

    # Initialize server
    mcp_server = SecLlamaMCPServer()

    # Run stdio transport
    await run_stdio_transport(mcp_server.server)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stdio transport stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

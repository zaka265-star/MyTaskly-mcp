#!/usr/bin/env python
"""
Run the MyTaskly MCP server with all registered tools.

Usage:
    python main.py              # Run MCP server in SSE mode (HTTP server)
"""

import os
from src.core.server import mcp
from src.config import settings


if __name__ == "__main__":
    # Get port from environment variable (Railway sets this)
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    # Run the MCP server in SSE mode for Railway deployment
    print(f"[+] Starting MCP server in SSE mode on {host}:{port}...")
    print("[+] Ready to accept HTTP connections\n")

    # Run with uvicorn in SSE mode
    mcp.run(transport="sse", host=host, port=port)

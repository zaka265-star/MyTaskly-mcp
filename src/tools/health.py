"""MCP health check tool."""

from typing import Dict, Any
from src.client import health_client
from src.config import settings


async def health_check() -> Dict[str, Any]:
    """
    Check health status of MCP server and FastAPI backend.

    This tool does NOT require authentication and can be used to verify
    that both the MCP server and the underlying FastAPI server are operational.

    Returns:
        {
            "mcp_server": "healthy",
            "fastapi_server": "healthy" | "unhealthy",
            "fastapi_url": "http://localhost:8080",
            "fastapi_details": {"status": "healthy", "code": 200}
        }

    Example usage:
        User: "Il server funziona?"
        Bot calls: health_check()
        Bot response: "✅ Tutti i servizi sono operativi"
    """
    fastapi_health = await health_client.health_check()

    return {
        "mcp_server": "healthy",
        "fastapi_server": fastapi_health.get("status", "unknown"),
        "fastapi_url": settings.fastapi_base_url,
        "fastapi_details": fastapi_health
    }

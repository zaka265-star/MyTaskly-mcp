"""HTTP client for health check endpoints."""

from typing import Dict, Any
from .base import BaseClient


class HealthClient(BaseClient):
    """Client for health check endpoints."""

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if FastAPI server is healthy.

        Returns:
            Health status dictionary with:
            - status: "healthy" or "unhealthy"
            - code: HTTP status code
            - error: Error message (if unhealthy)
        """
        try:
            return await self._get_no_auth("/health")
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# Global client instance
health_client = HealthClient()
